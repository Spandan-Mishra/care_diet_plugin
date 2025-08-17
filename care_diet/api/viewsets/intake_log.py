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
