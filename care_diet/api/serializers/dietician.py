import datetime
from pydantic import UUID4
from rest_framework import serializers
from care.emr.models.encounter import Encounter
from care.emr.models.patient import Patient
from care_diet.models.nutrition_order import NutritionOrder
from care.emr.resources.base import EMRResource
from care.facility.models import Facility
from care.emr.models.location import FacilityLocation

class DieticianOrderListSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    facility = serializers.PrimaryKeyRelatedField(read_only=True)
    current_location = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Encounter
        fields = ["id", "patient", "facility", "current_location", "status"]


class NutritionOrderCreateSpec(EMRResource):
    __model__ = NutritionOrder
    __exclude__ = ["patient", "encounter", "facility", "location", "prescribed_by"]

    patient: UUID4
    encounter: UUID4
    facility: UUID4
    location: UUID4

    service_type: str
    products: list
    datetime: datetime.datetime
    status: str
    schedule: dict
    note: str | None = None

    def perform_extra_deserialization(self, is_update, obj):
        obj.patient = Patient.objects.get(external_id=self.patient)
        obj.encounter = Encounter.objects.get(external_id=self.encounter)
        obj.facility = Facility.objects.get(external_id=self.facility)
        obj.location = FacilityLocation.objects.get(external_id=self.location)
