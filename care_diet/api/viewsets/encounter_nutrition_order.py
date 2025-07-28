from rest_framework import viewsets, mixins
from care_diet.models import NutritionOrder
from ..serializers.encounter_nutrition_order import EncounterNutritionOrderSerializer

class EncounterNutritionOrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Lists all Nutrition Orders for a specific Encounter.
    This version correctly filters by the Encounter's UUID (external_id).
    """
    serializer_class = EncounterNutritionOrderSerializer
    queryset = NutritionOrder.objects.filter(deleted=False)

    def get_queryset(self):
        qs = super().get_queryset()
        encounter_uuid = self.request.query_params.get("encounter")

        if encounter_uuid:
            return qs.filter(encounter__external_id=encounter_uuid)

        return qs.none()
