from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet

app_name = "products"

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = router.urls
