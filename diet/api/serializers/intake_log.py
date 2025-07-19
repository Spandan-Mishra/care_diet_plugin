from rest_framework import serializers
from care_diet_plugin.diet.models.nutrition_intake import NutritionIntake

class IntakeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionIntake
        fields = [
            "id",
            "patient",
            "encounter",
            "logged_by",
            "facility",
            "location",
            "service_type",
            "status",
            "status_reason",
            "intake_items",
            "occurrence_datetime",
            "note",
        ]
