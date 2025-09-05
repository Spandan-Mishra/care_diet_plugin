from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from care.emr.api.viewsets.charge_item import ChargeItemViewSet as BaseChargeItemViewSet
from care.emr.models import ChargeItem
from care.facility.models import Facility
from care.security.authorization.base import AuthorizationController


class ChargeItemViewSet(BaseChargeItemViewSet):
    """
    Care Diet specific ChargeItem ViewSet.
    Extends the main EMR ChargeItemViewSet with diet-specific filtering.
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
        # Get base queryset without facility filtering (skip parent's get_queryset if needed)
        base_queryset = super(BaseChargeItemViewSet, self).get_queryset()

        # Handle facility filtering from query parameter
        facility_id = self.request.query_params.get("facility")
        if facility_id:
            facility_obj = get_object_or_404(Facility, external_id=facility_id)
            # Filter by facility - charge items are linked to encounters which have facilities
            base_queryset = base_queryset.filter(encounter__patient__facility=facility_obj)

        # Filter by service resource type (e.g., nutrition_order)
        service_resource = self.request.query_params.get("service_resource")
        service_resource_id = self.request.query_params.get("service_resource_id")

        if service_resource and service_resource_id:
            # Filter for charge items related to specific service resources
            base_queryset = base_queryset.filter(
                service_resource=service_resource,
                service_resource_id=service_resource_id
            )
        elif service_resource:
            # Filter by service resource type only
            base_queryset = base_queryset.filter(service_resource=service_resource)

        return base_queryset
