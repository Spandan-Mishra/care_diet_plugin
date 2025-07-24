from rest_framework import serializers
from care_diet.models.nutrition_intake import NutritionIntake
from care.emr.models.patient import Patient
from care.emr.models.encounter import Encounter
from care.facility.models import Facility, FacilityLocation

class IntakeLogSerializer(serializers.ModelSerializer):

    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source="patient", to_field="external_id"
    )
    encounter = serializers.PrimaryKeyRelatedField(
        queryset=Encounter.objects.all(), source="encounter", to_field="external_id"
    )
    facility = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(), source="facility", to_field="external_id"
    )
    location = serializers.PrimaryKeyRelatedField(
        queryset=FacilityLocation.objects.all(), source="location", to_field="external_id"
    )

    logged_by = serializers.PrimaryKeyRelatedField(read_only=True)

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
