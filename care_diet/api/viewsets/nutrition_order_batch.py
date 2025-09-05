from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from care_diet.models import NutritionOrder, NutritionProduct
from care.emr.models import Patient, Encounter, FacilityLocation, Account, ChargeItem
from care.emr.resources.charge_item.spec import ChargeItemStatusOptions
from care.emr.resources.charge_item.apply_charge_item_definition import apply_charge_item_definition
from care.emr.resources.account.default_account import get_default_account
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

                        # Create billing using the same pattern as the main serializer
                        for product in products:
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
            # Use the standard billing flow like ActivityDefinition -> ServiceRequest
            account = get_default_account(nutrition_order.patient, nutrition_order.facility)

            # Apply charge item definition using the standard function
            charge_item = apply_charge_item_definition(
                product.charge_item_definition,
                nutrition_order.encounter,
                account,
                quantity=1.0  # Default quantity, could be made configurable
            )

            # Set nutrition order specific fields
            charge_item.service_resource = "nutrition_order"
            charge_item.service_resource_id = str(nutrition_order.external_id)
            charge_item.title = f"Nutrition Order - {product.name}"
            charge_item.description = f"Nutrition order for {product.name} ({product.code})"
            charge_item.save()

            return charge_item

        except Exception as e:
            # Log error but don't fail the order creation
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create charge item for nutrition order {nutrition_order.external_id}, product {product.external_id}: {e}")
            return None
