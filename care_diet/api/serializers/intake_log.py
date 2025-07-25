import datetime
from pydantic import UUID4
from rest_framework import serializers
from care_diet.models.nutrition_intake import NutritionIntake
from care.emr.resources.base import EMRResource
from care.emr.models.patient import Patient
from care.emr.models.encounter import Encounter
from care.facility.models import Facility
from care.emr.models.location import FacilityLocation

class NutritionIntakeCreateSpec(EMRResource):
    __model__ = NutritionIntake
    __exclude__ = ["patient", "encounter", "facility", "location", "logged_by"]

    patient: UUID4
    encounter: UUID4
    facility: UUID4
    location: UUID4

    service_type: str
    status: str
    status_reason: str | None = None
    intake_items: list
    occurrence_datetime: datetime.datetime
    note: str | None = None

    def perform_extra_deserialization(self, is_update, obj):
        obj.patient = Patient.objects.get(external_id=self.patient)
        obj.encounter = Encounter.objects.get(external_id=self.encounter)
        obj.facility = Facility.objects.get(external_id=self.facility)
        obj.location = FacilityLocation.objects.get(external_id=self.location)
