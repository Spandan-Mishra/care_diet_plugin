from rest_framework import viewsets, mixins
from care_diet_plugin.diet.models.nutrition_order import NutritionOrder
from care_diet_plugin.diet.api.serializers.encounter_nutrition_order import EncounterNutritionOrderSerializer

class EncounterNutritionOrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EncounterNutritionOrderSerializer
    queryset = NutritionOrder.objects.all()

    def get_queryset(self):
        encounter_id = self.request.query_params.get("encounter")
        if encounter_id:
            return NutritionOrder.objects.filter(encounter_id=encounter_id)
        return NutritionOrder.objects.none()
