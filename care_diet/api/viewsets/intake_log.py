from rest_framework import viewsets
from care_diet.models import NutritionIntake
from care_diet.api.serializers.intake_log import NutritionIntakeSerializer, NutritionIntakeListSerializer

class IntakeLogViewSet(viewsets.ModelViewSet):
    """Creates and lists Nutrition Intake logs."""
    queryset = NutritionIntake.objects.all().select_related(
        "patient", "encounter", "encounter__current_location", "logged_by", "facility"
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return NutritionIntakeListSerializer
        return NutritionIntakeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by facility if provided
        facility = self.request.query_params.get('facility')
        if facility:
            queryset = queryset.filter(facility=facility)

        # Filter by location if provided
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(encounter__current_location=location)

        # Filter by nutrition order if provided
        nutrition_order = self.request.query_params.get('nutrition_order')
        if nutrition_order:
            queryset = queryset.filter(nutrition_order=nutrition_order)

        return queryset
