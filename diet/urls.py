from rest_framework.routers import DefaultRouter

from diet.api.viewsets.diet import HelloViewset

router = DefaultRouter()

router.register("diet", HelloViewset, basename="diet__diet")

urlpatterns = router.urls
