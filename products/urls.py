from django.urls import path, include

# from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from products.views import ProductsViewset


# create router
router = DefaultRouter()
router.register("all-products", ProductsViewset, basename="all-products")

urlpatterns = [
    path("", include(router.urls))
    # path("products/", ProductView.as_view(), name="all-products")
]
