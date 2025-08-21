from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from care_diet.models import NutritionIntake
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
