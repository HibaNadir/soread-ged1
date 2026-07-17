from rest_framework.routers import DefaultRouter
from .views import SpaceViewSet

router = DefaultRouter()
router.register("spaces", SpaceViewSet, basename="spaces")

urlpatterns = router.urls