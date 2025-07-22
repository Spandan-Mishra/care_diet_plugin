from django.db import models
from care.facility.models import Facility
from care.users.models import User
from care.emr.models.encounter import Encounter
from care.emr.models.patient import Patient
from care.emr.models.location import FacilityLocation

class NutritionIntake(models.Model):
    STATUS_CHOICES = [
        ("preparation", "Preparation"),
        ("in-progress", "In Progress"),
        ("not-done", "Not Done"),
        ("on-hold", "On Hold"),
        ("stopped", "Stopped"),
        ("completed", "Completed"),
        ("entered-in-error", "Entered In Error"),
        ("unknown", "Unknown"),
    ]
    SERVICE_TYPE_CHOICES = [
        ("food", "Food"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    encounter = models.ForeignKey(Encounter, on_delete=models.PROTECT)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    location = models.ForeignKey(FacilityLocation, on_delete=models.PROTECT)
    service_type = models.CharField(max_length=32, choices=SERVICE_TYPE_CHOICES, default="food")

    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    status_reason = models.CharField(max_length=255, null=True, blank=True)
    intake_items = models.JSONField()
    occurrence_datetime = models.DateTimeField()
    note = models.TextField(null=True, blank=True)
