from rest_framework import serializers
from care_diet.models import NutritionOrder

class CanteenOrderUpdateSerializer(serializers.ModelSerializer):
    """A simple serializer for the Canteen to update only the order status."""
    class Meta:
        model = NutritionOrder
        fields = ("status",)
