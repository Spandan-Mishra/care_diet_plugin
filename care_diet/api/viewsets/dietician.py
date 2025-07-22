from rest_framework import viewsets, mixins
from care.emr.models.encounter import Encounter
from care_diet_plugin.diet.models.nutrition_order import NutritionOrder
from care_diet_plugin.diet.api.serializers.dietician import DieticianOrderListSerializer, DieticianMealSerializer
from care.facility.models import Facility

class DieticianOrderListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DieticianOrderListSerializer
    queryset = Encounter.objects.all()

    def get_queryset(self):
        facility_external_id = self.request.query_params.get("facility")
        facility = Facility.objects.get(external_id=facility_external_id)
        encounters_with_orders = NutritionOrder.objects.values_list("encounter_id", flat=True)
        return Encounter.objects.filter(facility=facility).exclude(id__in=encounters_with_orders)

class DieticianMealViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = NutritionOrder.objects.all()
    serializer_class = DieticianMealSerializer
