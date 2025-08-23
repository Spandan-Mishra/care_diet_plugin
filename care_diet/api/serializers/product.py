from rest_framework import serializers
from care_diet.models import NutritionProduct
from care.facility.models import Facility
from care.emr.models import FacilityLocation, ChargeItemDefinition

class NutritionProductSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and managing Nutrition Products.
    """
    id = serializers.UUIDField(source="external_id", read_only=True)
    facility = serializers.SlugRelatedField(
        slug_field="external_id", queryset=Facility.objects.all()
    )
    location = serializers.SlugRelatedField(
        slug_field="external_id", queryset=FacilityLocation.objects.all()
    )
    charge_item_definition = serializers.SlugRelatedField(
        slug_field="external_id",
        queryset=ChargeItemDefinition.objects.all(),
        required=False,
        allow_null=True
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
            "charge_item_definition",
        ]
        read_only_fields = ("id",)
