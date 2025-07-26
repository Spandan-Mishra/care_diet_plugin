from rest_framework import serializers
from care_diet.models import NutritionOrder, NutritionProduct
from care.users.models import User
from care.emr.models import Patient, Encounter, FacilityLocation
from care.facility.models import Facility

class DieticianEncounterSerializer(serializers.ModelSerializer):
    """Lists encounters that are waiting for a nutrition order."""
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    # The 'id' of an EMRBaseModel is its external_id (UUID) by default in DRF
    current_location_id = serializers.UUIDField(source="current_location.external_id", read_only=True, default=None)

    class Meta:
        model = Encounter
        fields = ("id", "patient_name", "status", "current_location_id")


class NutritionOrderSerializer(serializers.ModelSerializer):
    """
    Handles creating and displaying a full Nutrition Order.
    This is the definitive, working version.
    """
    # These fields accept UUIDs as input because of slug_field.
    patient = serializers.SlugRelatedField(slug_field="external_id", queryset=Patient.objects.all())
    encounter = serializers.SlugRelatedField(slug_field="external_id", queryset=Encounter.objects.all())
    facility = serializers.SlugRelatedField(slug_field="external_id", queryset=Facility.objects.all())
    location = serializers.SlugRelatedField(slug_field="external_id", queryset=FacilityLocation.objects.all())

    # This field will be automatically set and is not required in the request body.
    prescribed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    # This handles the many-to-many relationship with products using their UUIDs.
    products = serializers.SlugRelatedField(
        slug_field="external_id",
        queryset=NutritionProduct.objects.all(),
        many=True,
        required=False # This makes the field optional.
    )

    class Meta:
        model = NutritionOrder
        fields = "__all__"
        # The user cannot provide these fields; they are set by the system.
        read_only_fields = ("id", "external_id", "prescribed_by", "created_date", "modified_date", "deleted")

    def create(self, validated_data):
        # This is the simplest, most correct way to handle creation.
        # We add the user to the validated data before the object is created.
        validated_data["prescribed_by"] = self.context["request"].user
        # We do NOT manually set 'deleted'. The EMRBaseModel will handle it.
        return super().create(validated_data)
