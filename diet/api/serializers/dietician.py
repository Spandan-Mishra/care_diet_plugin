from rest_framework import serializers
from care.emr.models.encounter import Encounter
from care_diet_plugin.diet.models.nutrition_order import NutritionOrder

class DieticianOrderListSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    facility = serializers.PrimaryKeyRelatedField(read_only=True)
    current_location = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Encounter
        fields = [
            "id",
            "patient",
            "facility",
            "current_location",
            "status",
        ]

class DieticianMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionOrder
        fields = [
            "id",
            "encounter",
            "patient",
            "prescribed_by",
            "facility",
            "location",
            "service_type",
            "products",
            "datetime",
            "status",
            "schedule",
            "note",
        ]
