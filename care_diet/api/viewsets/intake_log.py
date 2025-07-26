from rest_framework import viewsets
from care_diet.models import NutritionIntake
from care_diet.api.serializers.intake_log import NutritionIntakeSerializer

class IntakeLogViewSet(viewsets.ModelViewSet):
    """Creates and lists Nutrition Intake logs."""
    queryset = NutritionIntake.objects.all()
    serializer_class = NutritionIntakeSerializer
