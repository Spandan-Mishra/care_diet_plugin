from django.db import models
from care.facility.models import Facility
from care.users.models import User
from care.emr.models.patient import Patient
from care.emr.models.location import FacilityLocation

class NutritionOrder(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("on-hold", "On Hold"),
        ("entered-in-error", "Entered In Error"),
        ("ended", "Ended"),
        ("completed", "Completed"),
        ("revoked", "Revoked"),
        ("unknown", "Unknown"),
    ]
    SERVICE_TYPE_CHOICES = [
        ("food", "Food"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    prescribed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    location = models.ForeignKey(FacilityLocation, on_delete=models.PROTECT)
    service_type = models.CharField(max_length=32, choices=SERVICE_TYPE_CHOICES, default="food")
    products = models.ManyToManyField("NutritionProduct", related_name="orders")

    datetime = models.DateTimeField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    schedule = models.JSONField(help_text="FHIR Timing object")
    note = models.TextField(null=True, blank=True)
