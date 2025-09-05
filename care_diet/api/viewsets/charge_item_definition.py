from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from care.emr.api.viewsets.charge_item_definition import (
    ChargeItemDefinitionViewSet as BaseChargeItemDefinitionViewSet
)
from care.facility.models import Facility
from care.security.authorization.base import AuthorizationController


class ChargeItemDefinitionViewSet(BaseChargeItemDefinitionViewSet):
    """
    Care Diet specific ChargeItemDefinition ViewSet.
    Extends the main EMR ChargeItemDefinitionViewSet with diet-specific filtering.
    """

    def get_facility_obj(self):
        """Override to get facility from query parameter instead of URL path."""
        facility_id = self.request.query_params.get("facility")
        if facility_id:
            return get_object_or_404(Facility, external_id=facility_id)
        # If no facility in query params, try to get from URL path (fallback to parent behavior)
        return super().get_facility_obj()

    def get_queryset(self):
        """Override to handle facility filtering via query parameter."""
        # Get base queryset without facility filtering (skip parent's get_queryset)
        base_queryset = super(BaseChargeItemDefinitionViewSet, self).get_queryset()

        # Handle facility filtering from query parameter
        facility_id = self.request.query_params.get("facility")
        if facility_id:
            facility_obj = get_object_or_404(Facility, external_id=facility_id)

            # Check authorization
            if not AuthorizationController.call(
                "can_list_facility_charge_item_definition",
                self.request.user,
                facility_obj,
            ):
                raise PermissionDenied("Access Denied to Charge Item Definition")

            # Filter by facility
            base_queryset = base_queryset.filter(facility=facility_obj)

        # Apply additional filters
        status = self.request.query_params.get("status")
        if status:
            base_queryset = base_queryset.filter(status=status)

        return base_queryset
