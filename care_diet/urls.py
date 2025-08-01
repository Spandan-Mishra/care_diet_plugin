from care_diet.api.viewsets.product import NutritionProductViewSet
from django.urls import path
from rest_framework.routers import SimpleRouter
from care_diet.api.viewsets.canteen import CanteenOrderViewSet
from care_diet.api.viewsets.dietician import DieticianOrderListViewSet, DieticianMealViewSet
from care_diet.api.viewsets.intake_log import IntakeLogViewSet
from care_diet.api.viewsets.encounter_nutrition_order import EncounterNutritionOrderViewSet
from care_diet.api.viewsets.diet import DietViewset

class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"

router = OptionalSlashRouter()
router.register("products", NutritionProductViewSet, basename="diet__nutrition-product")
router.register("dietician-orders", DieticianOrderListViewSet, basename="diet__dietician_orders")
router.register("dietician-meals", DieticianMealViewSet, basename="diet__dietician_meals")
router.register("canteen-orders", CanteenOrderViewSet, basename="diet__canteen_orders")
router.register("intake-logs", IntakeLogViewSet, basename="diet__intake_logs")
router.register("encounter-nutrition-orders", EncounterNutritionOrderViewSet, basename="diet__encounter_nutrition_orders")
router.register("diet", DietViewset, basename="diet__diet")

urlpatterns = router.urls
