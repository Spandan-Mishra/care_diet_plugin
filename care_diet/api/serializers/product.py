from rest_framework import serializers
from care_diet.models import NutritionProduct
from care.facility.models import Facility
from care.emr.models import FacilityLocation

class NutritionProductSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and managing Nutrition Products.
    """
    facility = serializers.SlugRelatedField(
        slug_field="external_id", queryset=Facility.objects.all()
    )
    location = serializers.SlugRelatedField(
        slug_field="external_id", queryset=FacilityLocation.objects.all()
    )

    class Meta:
        model = NutritionProduct
        fields = [
            "id",
            "name",
            "code",
            "quantity",
            "calories",
            "allergens",
            "status",
            "note",
            "facility",
            "location",
            "service_type",
        ]
        read_only_fields = ("id",)
