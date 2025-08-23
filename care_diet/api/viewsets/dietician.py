from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from care_diet.models import NutritionOrder
from care.emr.models import Encounter, Account, ChargeItem
from care.emr.resources.charge_item.spec import ChargeItemStatusOptions
from care.facility.models import Facility
from care_diet.api.serializers.dietician import DieticianEncounterSerializer, NutritionOrderSerializer

class DieticianOrderListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Lists Encounters that DO NOT yet have a Nutrition Order."""
    serializer_class = DieticianEncounterSerializer

    def get_queryset(self):
        facility_id = self.request.query_params.get("facility")
        if not facility_id:
            return Encounter.objects.none()

        facility = Facility.objects.get(external_id=facility_id)
        encounters_with_orders = NutritionOrder.objects.filter(facility=facility).values_list("encounter_id", flat=True).distinct()

        return Encounter.objects.filter(facility=facility).exclude(id__in=encounters_with_orders).select_related("patient", "current_location")

class DieticianMealViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Creates a new Nutrition Order."""
    queryset = NutritionOrder.objects.all()
    serializer_class = NutritionOrderSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create NutritionOrder and associated ChargeItem if needed."""
        # Create the nutrition order first
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            nutrition_order = NutritionOrder.objects.get(external_id=response.data['id'])

            # Create billing if product has charge item definition
            if (hasattr(nutrition_order, 'nutrition_product') and
                nutrition_order.nutrition_product and
                nutrition_order.nutrition_product.charge_item_definition):

                self._create_nutrition_order_charge_item(nutrition_order)

        return response

    def _create_nutrition_order_charge_item(self, nutrition_order):
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
                charge_item_definition=nutrition_order.nutrition_product.charge_item_definition,
                status=ChargeItemStatusOptions.billable.value,
                facility=nutrition_order.facility,
                title=f"Nutrition Order - {nutrition_order.nutrition_product.name}",
                description=f"Nutrition order for {nutrition_order.nutrition_product.name}",
            )

            return charge_item

        except Exception as e:
            # Log error but don't fail the order creation
            print(f"Failed to create charge item for nutrition order {nutrition_order.external_id}: {e}")
            return None
