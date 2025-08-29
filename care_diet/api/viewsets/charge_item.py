from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from care.emr.api.viewsets.charge_item import ChargeItemViewSet as BaseChargeItemViewSet
from care.emr.models import ChargeItem


class ChargeItemViewSet(BaseChargeItemViewSet):
    """
    Care Diet specific ChargeItem ViewSet.
    Extends the main EMR ChargeItemViewSet with diet-specific filtering.
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by facility if provided
        facility = self.request.query_params.get("facility")
        if facility:
            queryset = queryset.filter(encounter__patient__facility__external_id=facility)

        # Filter by service resource type (e.g., nutrition_order)
        service_resource = self.request.query_params.get("service_resource")
        service_resource_id = self.request.query_params.get("service_resource_id")

        if service_resource == "nutrition_order" and service_resource_id:
            # Filter for charge items related to nutrition orders
            queryset = queryset.filter(
                service_resource="nutrition_order",
                service_resource_id=service_resource_id
            )

        return queryset
