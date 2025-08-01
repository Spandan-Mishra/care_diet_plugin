from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from care_diet.models import NutritionProduct
from ..serializers.product import NutritionProductSerializer

class NutritionProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Nutrition Products.
    Provides full CRUD and a custom list-by-facility action.
    """
    queryset = NutritionProduct.objects.filter(deleted=False).order_by("name")
    serializer_class = NutritionProductSerializer
    lookup_field = "external_id"

    def list(self, request, *args, **kwargs):
        """
        Lists all Nutrition Products for a specific facility.
        Accessed via: GET /api/care_diet/products/?facility=<facility_uuid>
        """
        facility_uuid = request.query_params.get("facility")
        if not facility_uuid:
            return Response({"count": 0, "next": None, "previous": None, "results": []})

        queryset = self.get_queryset().filter(facility__external_id=facility_uuid)

        search_term = request.query_params.get("search")
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
