from rest_framework import serializers
from care_diet.models import NutritionOrder, NutritionProduct
from care.users.models import User
from care.emr.models import Patient, Encounter, FacilityLocation, Account, ChargeItem
from care.emr.resources.charge_item.spec import ChargeItemStatusOptions
from care.emr.resources.charge_item.apply_charge_item_definition import apply_charge_item_definition
from care.emr.resources.account.default_account import get_default_account
from care.facility.models import Facility
from django.db import transaction

class DieticianEncounterSerializer(serializers.ModelSerializer):
    """Lists encounters that are waiting for a nutrition order."""
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    current_location_id = serializers.UUIDField(source="current_location.external_id", read_only=True, default=None)

    class Meta:
        model = Encounter
        fields = ("id", "patient_name", "status", "current_location_id")


class NutritionOrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    patient = serializers.SlugRelatedField(slug_field="external_id", queryset=Patient.objects.all())
    encounter = serializers.SlugRelatedField(slug_field="external_id", queryset=Encounter.objects.all())
    facility = serializers.SlugRelatedField(slug_field="external_id", queryset=Facility.objects.all())
    location = serializers.SlugRelatedField(slug_field="external_id", queryset=FacilityLocation.objects.all())
    prescribed_by = serializers.PrimaryKeyRelatedField(read_only=True)
    products = serializers.SlugRelatedField(
        slug_field="external_id",
        queryset=NutritionProduct.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = NutritionOrder
        fields = "__all__"
        read_only_fields = ("id", "external_id", "prescribed_by", "created_date", "modified_date", "deleted")

    def create(self, validated_data):
        with transaction.atomic():
            product_data = validated_data.pop('products', [])
            validated_data["prescribed_by"] = self.context["request"].user

            order = NutritionOrder.objects.create(**validated_data)

            if product_data:
                order.products.set(product_data)

                # Create billing for each product with charge item definition
                self._create_charge_items_for_products(order, product_data)

            return order

    def _create_charge_items_for_products(self, nutrition_order, products):
        """Create ChargeItems for NutritionOrder based on products' ChargeItemDefinitions."""
        for product in products:
            if product.charge_item_definition:
                try:
                    # Use the same pattern as ActivityDefinition -> ServiceRequest
                    account = get_default_account(nutrition_order.patient, nutrition_order.facility)

                    # Apply charge item definition to create charge item
                    charge_item = apply_charge_item_definition(
                        product.charge_item_definition,
                        nutrition_order.encounter,
                        account,
                        quantity=1.0  # Default quantity, could be made configurable
                    )

                    # Set nutrition order specific fields
                    charge_item.service_resource = "nutrition_order"
                    charge_item.service_resource_id = str(nutrition_order.external_id)
                    charge_item.title = f"Nutrition Order - {product.name}"
                    charge_item.description = f"Nutrition order for {product.name} ({product.code})"
                    charge_item.save()

                except Exception as e:
                    # Log error but don't fail the order creation
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to create charge item for nutrition order {nutrition_order.external_id}, product {product.external_id}: {e}")
                    continue
