from django.db import models
from care.facility.models import Facility
from care.users.models import User
from care.emr.models.encounter import Encounter
from care.emr.models.patient import Patient



class NutritionOrder(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("on-hold", "On Hold"),
        ("revoked", "Revoked"),
        ("completed", "Completed"),
        ("entered-in-error", "Entered In Error"),
        ("unknown", "Unknown"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    prescribed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)

    datetime = models.DateTimeField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    schedule = models.JSONField()
    note = models.TextField(null=True, blank=True)


class NutritionProduct(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("entered-in-error", "Entered In Error"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    quantity = models.CharField(max_length=100)
    calories = models.IntegerField()
    allergens = models.JSONField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    note = models.TextField(null=True, blank=True)


class NutritionIntake(models.Model):
    STATUS_CHOICES = [
        ("in-progress", "In Progress"),
        ("completed", "Completed"),
        ("not-done", "Not Done"),
        ("entered-in-error", "Entered In Error"),
        ("unknown", "Unknown"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    encounter = models.ForeignKey(Encounter, on_delete=models.PROTECT)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)

    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    status_reason = models.CharField(max_length=255, null=True, blank=True)
    intake_items = models.JSONField()
    occurrence_datetime = models.DateTimeField()
    note = models.TextField(null=True, blank=True)
