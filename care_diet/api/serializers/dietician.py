from rest_framework import serializers
from care.emr.models.encounter import Encounter
from care_diet.models.nutrition_order import NutritionOrder
from care.emr.models.patient import Patient
from care.facility.models import Facility, FacilityLocation

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

    prescribed_by = serializers.PrimaryKeyRelatedField(read_only=True)

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
