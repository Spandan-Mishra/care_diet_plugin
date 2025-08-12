from rest_framework import viewsets, mixins
from care_diet.models import NutritionOrder
from ..serializers.dietician import NutritionOrderSerializer
from ..serializers.canteen import CanteenOrderUpdateSerializer

class CanteenOrderViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Lists and updates status of Nutrition Orders for the Canteen.
    This version correctly handles both LIST and UPDATE actions.
    """
    queryset = NutritionOrder.objects.exclude(status__in=["completed", "revoked"]).select_related("patient", "encounter")
    lookup_field = "external_id"

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CanteenOrderUpdateSerializer
        return NutritionOrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            facility_id = self.request.query_params.get("facility")
            location_id = self.request.query_params.get("location")

            if facility_id:
                qs = qs.filter(facility__external_id=facility_id)

            if location_id:
                qs = qs.filter(location__external_id=location_id)

            if not facility_id:
                return qs.none()

        return qs
