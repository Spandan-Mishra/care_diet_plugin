from rest_framework import viewsets, mixins
from care_diet.models.nutrition_order import NutritionOrder
from care_diet.api.serializers.canteen import CanteenOrderSerializer

class CanteenOrderViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = CanteenOrderSerializer
    queryset = NutritionOrder.objects.all()

    def get_queryset(self):
        location_id = self.request.query_params.get("location")
        facility_id = self.request.query_params.get("facility")
        qs = NutritionOrder.objects.all()
        if location_id:
            qs = qs.filter(location_id=location_id)
        if facility_id:
            qs = qs.filter(facility_id=facility_id)
        return qs
