from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from care_diet.models import NutritionIntake, NutritionOrder
from care.emr.models import Account, ChargeItem
from care.emr.resources.charge_item.spec import ChargeItemStatusOptions
from care_diet.api.serializers.intake_log import NutritionIntakeSerializer, NutritionIntakeListSerializer

class IntakeLogViewSet(viewsets.ModelViewSet):
    """Creates and lists Nutrition Intake logs."""
    queryset = NutritionIntake.objects.all().select_related(
        "patient", "encounter", "encounter__current_location", "logged_by", "facility"
    )
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return NutritionIntakeListSerializer
        return NutritionIntakeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by facility if provided
        facility = self.request.query_params.get('facility')
        if facility:
            queryset = queryset.filter(facility__external_id=facility)

        # Filter by location if provided
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(encounter__current_location__external_id=location)

        # Filter by encounter if provided
        encounter = self.request.query_params.get('encounter')
        if encounter:
            queryset = queryset.filter(encounter__external_id=encounter)

        # Filter by nutrition order if provided
        # nutrition_order = self.request.query_params.get('nutrition_order')
        # if nutrition_order:
        #     queryset = queryset.filter(nutrition_order__external_id=nutrition_order)

        # Order by occurrence_datetime descending (most recent first)
        return queryset.order_by('-occurrence_datetime')

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create NutritionIntake and handle billing if needed."""
        # Create the nutrition intake first
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            nutrition_intake = NutritionIntake.objects.get(external_id=response.data['id'])

            # Check if billing is needed for this intake
            charge_item = self._create_intake_charge_item_if_needed(nutrition_intake)
            if charge_item:
                nutrition_intake.charge_item = charge_item
                nutrition_intake.save(update_fields=['charge_item'])

        return response

    def _create_intake_charge_item_if_needed(self, nutrition_intake):
        """
        Create ChargeItem for NutritionIntake if:
        1. The intake is not linked to a nutrition order, OR
        2. The linked nutrition order doesn't have billing (no charge item definition)
        """
        try:
            # Check if this intake is linked to a nutrition order with billing
            if (nutrition_intake.nutrition_order and
                nutrition_intake.nutrition_order.nutrition_product and
                nutrition_intake.nutrition_order.nutrition_product.charge_item_definition):

                # Check if the nutrition order already has a charge item
                existing_charge_items = ChargeItem.objects.filter(
                    service_resource="nutrition_order",
                    service_resource_id=str(nutrition_intake.nutrition_order.external_id)
                )

                if existing_charge_items.exists():
                    # Order is already billed, no need to create separate intake billing
                    return None

            # Check if the nutrition product itself has a charge item definition
            nutrition_product = None
            if nutrition_intake.nutrition_order:
                nutrition_product = nutrition_intake.nutrition_order.nutrition_product

            if not nutrition_product or not nutrition_product.charge_item_definition:
                # No billing definition available
                return None

            # Get or create account for patient
            account, created = Account.objects.get_or_create(
                patient=nutrition_intake.patient,
                defaults={
                    'status': 'active',
                    'facility': nutrition_intake.facility,
                }
            )

            # Create ChargeItem for the intake
            charge_item = ChargeItem.objects.create(
                account=account,
                patient=nutrition_intake.patient,
                encounter=nutrition_intake.encounter,
                service_resource="nutrition_intake",
                service_resource_id=str(nutrition_intake.external_id),
                charge_item_definition=nutrition_product.charge_item_definition,
                status=ChargeItemStatusOptions.billable.value,
                facility=nutrition_intake.facility,
                title=f"Nutrition Intake - {nutrition_product.name}",
                description=f"Nutrition intake for {nutrition_product.name}",
            )

            return charge_item

        except Exception as e:
            # Log error but don't fail the intake creation
            print(f"Failed to create charge item for nutrition intake {nutrition_intake.external_id}: {e}")
            return None
