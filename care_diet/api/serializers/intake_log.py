from rest_framework import serializers
from care_diet.models import NutritionIntake
from care.emr.models import Patient, Encounter, FacilityLocation
from care.facility.models import Facility

class NutritionIntakeSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing a Nutrition Intake log."""
    patient = serializers.SlugRelatedField(slug_field="external_id", queryset=Patient.objects.all())
    encounter = serializers.SlugRelatedField(slug_field="external_id", queryset=Encounter.objects.all())
    facility = serializers.SlugRelatedField(slug_field="external_id", queryset=Facility.objects.all())
    location = serializers.SlugRelatedField(slug_field="external_id", queryset=FacilityLocation.objects.all())
    logged_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NutritionIntake
        fields = "__all__"
        read_only_fields = ("logged_by",)

    def create(self, validated_data):
        validated_data["logged_by"] = self.context["request"].user
        validated_data["deleted"] = False
        return super().create(validated_data)
