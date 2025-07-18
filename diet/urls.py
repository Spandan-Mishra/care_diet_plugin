from django.urls import path
from rest_framework.routers import SimpleRouter
from care_diet_plugin.diet.api.viewsets.dietician import DieticianOrderListViewSet, DieticianMealViewSet
from care_diet_plugin.diet.api.viewsets.canteen import CanteenOrderViewSet
from diet.api.viewsets.diet import HelloViewset

class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"

router = OptionalSlashRouter()
router.register("dietician-orders", DieticianOrderListViewSet, basename="diet__dietician_orders")
router.register("dietician-meals", DieticianMealViewSet, basename="diet__dietician_meals")
router.register("canteen-orders", CanteenOrderViewSet, basename="diet__canteen_orders")
router.register("diet", HelloViewset, basename="diet__diet")

urlpatterns = router.urls
