from rest_framework import serializers
from care_diet.models.nutrition_order import NutritionOrder

class EncounterNutritionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionOrder
        fields = [
            "id",
            "patient",
            "prescribed_by",
            "facility",
            "location",
            "encounter",
            "products",
            "datetime",
            "status",
            "schedule",
            "note",
        ]
