from rest_framework import viewsets
from care_diet.models import NutritionProduct
from ..serializers.product import NutritionProductSerializer

class NutritionProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for creating, viewing, and managing Nutrition Products.
    """
    queryset = NutritionProduct.objects.filter(deleted=False)
    serializer_class = NutritionProductSerializer
    lookup_field = "external_id" # Use UUID for detail view URLs
