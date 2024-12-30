from django.urls import path, include

from rest_framework.routers import SimpleRouter

from electronics.apps import ElectronicsConfig
from electronics.views import NetworkObjectViewSet, ProductViewSet

app_name = ElectronicsConfig.name

router = SimpleRouter()
router.register("products", ProductViewSet)
router.register("networkobjects", NetworkObjectViewSet)

urlpatterns = [
    path("", include(router.urls)),
]