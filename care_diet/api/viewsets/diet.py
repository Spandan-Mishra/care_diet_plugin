from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from diet.api.serializers.diet import DietSerializer
from diet.models.diet import Diet


class DietViewset(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    queryset = Diet.objects.all().order_by("-created_date")
    serializer_class = DietSerializer
    lookup_field = "external_id"
    permission_classes = [IsAuthenticated]
