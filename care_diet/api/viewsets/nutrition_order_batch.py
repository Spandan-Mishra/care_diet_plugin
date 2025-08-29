from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from care_diet.models import NutritionOrder, NutritionProduct
from care.emr.models import Patient, Encounter, FacilityLocation, Account, ChargeItem
from care.emr.resources.charge_item.spec import ChargeItemStatusOptions
from care.facility.models import Facility
from care_diet.api.serializers.dietician import NutritionOrderSerializer


class NutritionOrderBatchViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Batch endpoint for creating/updating nutrition orders.
    Used by the questionnaire system.
    """
    queryset = NutritionOrder.objects.all()
    serializer_class = NutritionOrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='upsert')
    @transaction.atomic
    def upsert(self, request, *args, **kwargs):
        """
        Upsert endpoint for nutrition orders.
        Expects a list of nutrition order datapoints.
        """
        datapoints = request.data.get('datapoints', [])

        if not datapoints:
            return Response(
                {"error": "No datapoints provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_orders = []

        for datapoint in datapoints:
            try:
                # Extract products from datapoint
                product_ids = datapoint.pop('products', [])

                # Set the prescribed_by to the current user
                datapoint['prescribed_by'] = request.user

                # Create the nutrition order
                serializer = self.get_serializer(data=datapoint)
                if serializer.is_valid():
                    nutrition_order = serializer.save()

                    # Set products
                    if product_ids:
                        products = NutritionProduct.objects.filter(external_id__in=product_ids)
                        nutrition_order.products.set(products)

                    # Create billing if products have charge item definitions
                    for product in nutrition_order.products.all():
                        if product.charge_item_definition:
                            self._create_nutrition_order_charge_item(nutrition_order, product)

                    created_orders.append(serializer.data)
                else:
                    return Response(
                        {"error": f"Invalid data: {serializer.errors}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except Exception as e:
                return Response(
                    {"error": f"Failed to create nutrition order: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {"created_orders": created_orders},
            status=status.HTTP_201_CREATED
        )

    def _create_nutrition_order_charge_item(self, nutrition_order, product):
        """Create ChargeItem for NutritionOrder based on product's ChargeItemDefinition."""
        try:
            # Get or create account for patient
            account, created = Account.objects.get_or_create(
                patient=nutrition_order.patient,
                defaults={
                    'status': 'active',
                    'facility': nutrition_order.facility,
                }
            )

            # Create ChargeItem
            charge_item = ChargeItem.objects.create(
                account=account,
                patient=nutrition_order.patient,
                encounter=nutrition_order.encounter,
                service_resource="nutrition_order",
                service_resource_id=str(nutrition_order.external_id),
                charge_item_definition=product.charge_item_definition,
                status=ChargeItemStatusOptions.billable.value,
                facility=nutrition_order.facility,
                title=f"Nutrition Order - {product.name}",
                description=f"Nutrition order for {product.name}",
            )

            return charge_item

        except Exception as e:
            # Log error but don't fail the order creation
            print(f"Failed to create charge item for nutrition order {nutrition_order.external_id}: {e}")
            return None
