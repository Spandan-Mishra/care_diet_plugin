from rest_framework import serializers
from care_diet_plugin.diet.models.nutrition_order import NutritionOrder

class CanteenOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionOrder
        fields = [
            "id",
            "patient",
            "products",
            "status",
            "location",
            "facility",
            "datetime",
            "note",
        ]
