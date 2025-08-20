from rest_framework import serializers
from care_diet.models import NutritionIntake, NutritionOrder
from care.emr.models import Patient, Encounter, FacilityLocation
from care.facility.models import Facility

class NutritionIntakeSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing a Nutrition Intake log."""
    id = serializers.UUIDField(source="external_id", read_only=True)
    patient = serializers.SlugRelatedField(slug_field="external_id", queryset=Patient.objects.all())
    encounter = serializers.SlugRelatedField(slug_field="external_id", queryset=Encounter.objects.all())
    facility = serializers.SlugRelatedField(slug_field="external_id", queryset=Facility.objects.all())
    # nutrition_order = serializers.SlugRelatedField(slug_field="external_id", queryset=NutritionOrder.objects.all())
    logged_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NutritionIntake
        fields = (
            "id", "patient", "encounter", "facility", "logged_by",
            "service_type", "status", "status_reason", "intake_items",
            "occurrence_datetime", "note", "created_date", "modified_date"
        )
        read_only_fields = ("id", "logged_by", "created_date", "modified_date")

    def create(self, validated_data):
        validated_data["logged_by"] = self.context["request"].user
        validated_data["deleted"] = False
        return super().create(validated_data)


class IntakePatientDetailSerializer(serializers.Serializer):
    """Simple serializer for patient details in intake logs."""
    id = serializers.UUIDField(source="external_id")
    name = serializers.CharField()


class IntakeEncounterDetailSerializer(serializers.Serializer):
    """Simple serializer for encounter details in intake logs."""
    id = serializers.UUIDField(source="external_id")
    current_bed = serializers.CharField(source="current_location.name", allow_null=True)


class NutritionIntakeListSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for listing Nutrition Intake logs.
    Includes full patient and encounter details.
    """
    id = serializers.UUIDField(source="external_id", read_only=True)
    patient = IntakePatientDetailSerializer(read_only=True)
    encounter = IntakeEncounterDetailSerializer(read_only=True)
    logged_by = serializers.CharField(source="logged_by.username", read_only=True)
    facility = serializers.UUIDField(source="facility.external_id", read_only=True)
    # nutrition_order = serializers.UUIDField(source="nutrition_order.external_id", read_only=True)

    class Meta:
        model = NutritionIntake
        fields = (
            "id", "patient", "encounter", "facility", "logged_by",
            "service_type", "status", "status_reason", "intake_items",
            "occurrence_datetime", "note", "created_date", "modified_date"
        )
