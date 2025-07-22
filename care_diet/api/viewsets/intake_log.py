from rest_framework import viewsets, mixins
from care_diet_plugin.diet.models.nutrition_intake import NutritionIntake
from care_diet_plugin.diet.api.serializers.intake_log import IntakeLogSerializer

class IntakeLogViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = NutritionIntake.objects.all()
    serializer_class = IntakeLogSerializer
