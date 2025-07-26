from rest_framework import viewsets, mixins
from care_diet.models import NutritionOrder
from care_diet.api.serializers.dietician import NutritionOrderSerializer
from care_diet.api.serializers.canteen import CanteenOrderUpdateSerializer

class CanteenOrderViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Lists and updates status of Nutrition Orders for the Canteen."""
    queryset = NutritionOrder.objects.exclude(status__in=["completed", "revoked"]).select_related("patient")

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CanteenOrderUpdateSerializer
        return NutritionOrderSerializer

    def get_queryset(self):
        facility_id = self.request.query_params.get("facility")
        if facility_id:
            return self.queryset.filter(facility__external_id=facility_id)
        return self.queryset.none()
