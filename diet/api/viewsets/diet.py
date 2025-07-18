from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from diet.api.serializers.hello import HelloSerializer
from diet.models.hello import Hello


class HelloViewset(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    queryset = Hello.objects.all().order_by("-created_date")
    serializer_class = HelloSerializer
    lookup_field = "external_id"
    permission_classes = [IsAuthenticated]
