from django.urls import path, include

# from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewset, ProductsViewset, StoreViewset


# create router
router = DefaultRouter()
# register all products viewsets
router.register("all-products", ProductsViewset, basename="all-products")
# register store viewset
router.register("all-stores", StoreViewset, basename="all-stores")
# register all-stores/{store}/categories
router.register("categories", CategoryViewset, basename="categories")

urlpatterns = [
    path("", include(router.urls))
    # path("products/", ProductView.as_view(), name="all-products")
]
