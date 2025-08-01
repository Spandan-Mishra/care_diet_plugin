from care.emr.models.base import EMRBaseModel
from django.db import models
from care.facility.models import Facility
from care.emr.models.location import FacilityLocation

class NutritionProduct(EMRBaseModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("entered-in-error", "Entered In Error"),
    ]
    SERVICE_TYPE_CHOICES = [
        ("food", "Food"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    quantity = models.CharField(max_length=100)
    calories = models.IntegerField()

    allergens = models.JSONField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    note = models.TextField(null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    location = models.ForeignKey(FacilityLocation, on_delete=models.PROTECT)
    service_type = models.CharField(max_length=32, choices=SERVICE_TYPE_CHOICES, default="food")
