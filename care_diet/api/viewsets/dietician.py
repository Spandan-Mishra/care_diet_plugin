from rest_framework import viewsets, mixins
from care.emr.models.encounter import Encounter
from care_diet.models.nutrition_order import NutritionOrder
from care_diet.api.serializers.dietician import DieticianOrderListSerializer, NutritionOrderCreateSpec
from care.emr.api.viewsets.base import EMRCreateMixin, EMRListMixin
from care.facility.models import Facility

class DieticianOrderListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DieticianOrderListSerializer
    def get_queryset(self):
        # ...
        return Encounter.objects.filter(facility=facility).exclude(id__in=encounters_with_orders)


class DieticianMealViewSet(EMRCreateMixin, EMRListMixin, viewsets.GenericViewSet):
    database_model = NutritionOrder
    pydantic_model = NutritionOrderCreateSpec

    queryset = NutritionOrder.objects.all().select_related("patient", "facility", "location")

    def authorize_create(self, instance):
        instance.prescribed_by = self.request.user
