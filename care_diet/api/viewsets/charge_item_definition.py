from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from care.emr.api.viewsets.charge_item_definition import (
    ChargeItemDefinitionViewSet as BaseChargeItemDefinitionViewSet
)


class ChargeItemDefinitionViewSet(BaseChargeItemDefinitionViewSet):
    """
    Care Diet specific ChargeItemDefinition ViewSet.
    Extends the main EMR ChargeItemDefinitionViewSet with diet-specific filtering.
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by facility if provided
        facility = self.request.query_params.get("facility")
        if facility:
            queryset = queryset.filter(facility__external_id=facility)

        # Filter by status if provided
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        return queryset
