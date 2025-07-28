from rest_framework import serializers
from care_diet.models import NutritionOrder
from .product import NutritionProductSerializer

class EncounterNutritionOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Nutrition Orders on the encounter tab.
    Ensures all related object IDs are represented by their UUIDs.
    """
    id = serializers.UUIDField(source="external_id", read_only=True)
    patient = serializers.UUIDField(source="patient.external_id", read_only=True)
    prescribed_by = serializers.CharField(source="prescribed_by.username", read_only=True)
    facility = serializers.UUIDField(source="facility.external_id", read_only=True)
    location = serializers.UUIDField(source="location.external_id", read_only=True)
    encounter = serializers.UUIDField(source="encounter.external_id", read_only=True)
    products = NutritionProductSerializer(many=True, read_only=True)

    class Meta:
        model = NutritionOrder
        fields = (
            "id", "patient", "prescribed_by", "facility", "location", "encounter",
            "products", "datetime", "status", "schedule", "note"
        )
