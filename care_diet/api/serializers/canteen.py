from rest_framework import serializers
from care_diet.models import NutritionOrder
from .product import NutritionProductSerializer

class CanteenOrderUpdateSerializer(serializers.ModelSerializer):
    """A simple serializer for the Canteen to update only the order status."""
    class Meta:
        model = NutritionOrder
        fields = ("status",)


class PatientDetailSerializer(serializers.Serializer):
    """Simple serializer for patient details in canteen orders."""
    id = serializers.UUIDField(source="external_id")
    name = serializers.CharField()


class EncounterDetailSerializer(serializers.Serializer):
    """Simple serializer for encounter details in canteen orders."""
    id = serializers.UUIDField(source="external_id")
    current_bed = serializers.CharField(source="current_location.name", allow_null=True)


class CanteenOrderListSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for listing Nutrition Orders in the Canteen.
    Includes full patient, encounter, and product details.
    """
    id = serializers.UUIDField(source="external_id", read_only=True)
    patient = PatientDetailSerializer(read_only=True)
    encounter = EncounterDetailSerializer(read_only=True)
    prescribed_by = serializers.CharField(source="prescribed_by.username", read_only=True)
    facility = serializers.UUIDField(source="facility.external_id", read_only=True)
    location = serializers.UUIDField(source="location.external_id", read_only=True)
    products = NutritionProductSerializer(many=True, read_only=True)

    class Meta:
        model = NutritionOrder
        fields = (
            "id", "patient", "encounter", "prescribed_by", "facility", "location",
            "products", "datetime", "status", "schedule", "note", "service_type"
        )
