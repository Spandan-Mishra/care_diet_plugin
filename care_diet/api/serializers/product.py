from rest_framework import serializers
from care_diet.models import NutritionProduct
from care.facility.models import Facility
from care.emr.models import FacilityLocation

class NutritionProductSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and managing Nutrition Products.
    """
    # These fields will accept a UUID string on input.
    facility = serializers.SlugRelatedField(
        slug_field="external_id", queryset=Facility.objects.all()
    )
    location = serializers.SlugRelatedField(
        slug_field="external_id", queryset=FacilityLocation.objects.all()
    )

    class Meta:
        model = NutritionProduct
        # We explicitly list fields to control what can be sent/received.
        fields = [
            "id", # This will be the UUID on output
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
        # 'id' is the external_id because of EMRBaseModel.
        read_only_fields = ("id",)
