from rest_framework import viewsets, mixins
from care_diet.models import NutritionOrder
from care.emr.models import Encounter
from care.facility.models import Facility
from care_diet.api.serializers.dietician import DieticianEncounterSerializer, NutritionOrderSerializer

class DieticianOrderListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Lists Encounters that DO NOT yet have a Nutrition Order."""
    serializer_class = DieticianEncounterSerializer

    def get_queryset(self):
        facility_id = self.request.query_params.get("facility")
        if not facility_id:
            return Encounter.objects.none()

        facility = Facility.objects.get(external_id=facility_id)
        encounters_with_orders = NutritionOrder.objects.filter(facility=facility).values_list("encounter_id", flat=True).distinct()

        return Encounter.objects.filter(facility=facility).exclude(id__in=encounters_with_orders).select_related("patient", "current_location")

class DieticianMealViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Creates a new Nutrition Order."""
    queryset = NutritionOrder.objects.all()
    serializer_class = NutritionOrderSerializer

    def get_serializer_context(self):
        return {"request": self.request}
