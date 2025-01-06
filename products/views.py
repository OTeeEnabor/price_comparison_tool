from django.core.paginator import Paginator
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Store, Products
from .serializers import CategorySerializer, StoreSerializer, ProductSerializer


# Create your views here.
class StorePagination(PageNumberPagination):
    page_size = 10


class CategoryPagination(PageNumberPagination):
    page_size = 10


class ProductPagination(PageNumberPagination):
    page_size = 50


class CategoryViewset(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        # `queryset = Category.objects.all()` is retrieving all instances of the `Category` model from
        # the database. It fetches all the records from the `Category` table in the database and
        # returns them as a queryset, which can then be used to perform operations like filtering,
        # sorting, or pagination.
        queryset = Category.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        "Intended to return a single instance of  a model and not a list"
        # get list of stores in the database
        list_of_stores = list(Store.objects.all().values_list("store_name", flat=True))
        print(kwargs)
        # URl parameters
        params = kwargs
        store = params["pk"]
        # print(list_of_stores)
        if store not in list_of_stores:
            return Response(
                {
                    "message": "Store not present in database. Please check spelling if sure is in database."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # filter database by params
        filtered_categories = Category.objects.filter(
            category_store__store_name=params["pk"]
        )
        # serialize filtered products
        serialized_filtered_categories = CategorySerializer(
            filtered_categories, many=True
        )
        response = {
            "data": serialized_filtered_categories.data,
            "message": "Categories were successfully filtered.",
        }
        return Response(response)

    @action(detail=True, methods=["get"], url_path="products")
    def get_products(self, request, *args, **kwargs):
        # get store - should be in list of stores
        store_name = kwargs["pk"]
        # get query_parameter -> category
        category = request.GET.get("category")
        print(store_name)
        print(category)
        # get all products from store
        products = Products.objects.filter(
            product_store=store_name, product_category=category
        )
        # print(products)
        # serialize queryset
        serialized_filtered_products = ProductSerializer(products, many=True)

        response = {
            "data": serialized_filtered_products.data,
            "message": "successfully filtered the products based on category and store",
        }
        return Response(response, status=status.HTTP_200_OK)


class StoreViewset(viewsets.ModelViewSet):
    serializer_class = StoreSerializer

    def get_queryset(self):
        # limit this to 20 for now
        queryset = Store.objects.all()  # [:20]
        return queryset  # super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        # get query parameters
        query_params = request.query_params()
        params = kwargs
        print(params)
        return Response({})


class ProductsViewset(viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    pagination_class = ProductPagination

    def get_queryset(self):
        # limit this to 20 for now
        queryset = Products.objects.all()  # [:20]
        return queryset  # super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        # get parameter to be used to filter the database
        params = kwargs
        print(params)
        # filter databse by params
        filtered_products = Products.objects.filter(product_store=params["pk"])

        # serialize filtered products
        serialized_filtered_products = ProductSerializer(filtered_products, many=True)
        # print(filtered_products)
        response = {
            "data": serialized_filtered_products.data,
            "message": "products were successfully filtered.",
        }
        return Response(response)

    def create(self, request, *args, **kwargs):
        product_data = request.data

        # create a new product object
        new_product = Products.objects.create(
            product_name=product_data["product_name"],
            product_barcode=product_data["product_barcode"],
            product_date=product_data["product_date"],
            product_category=product_data["product_category"],
            product_price=product_data["product_price"],
            product_weight=product_data["product_weight"],
            product_url=product_data["product_url"],
            product_store=product_data["product_store"],
        )
        # ForeignModel.objects.get(product_data[category])
        # save the product object
        new_product.save()

        # serialize the data
        serialized_new_product = ProductSerializer(new_product)

        # response
        response = {
            "data": serialized_new_product.data,
            "message": "Product successfully added to database.",
        }
        return Response(response)

    def destroy(self, request, *args, **kwargs):
        user_logged_in = request.user
        if user_logged_in != "admin":
            response = {"message": "You do not have the permission for this action."}
            return Response(response)

        product = self.get_object()
        product.delete()

        response = {"message": "Product has been deleted."}
        return Response(response)


# class ProductView(APIView):
#     def get(self, request):
#         print(request.query_params)
#         try:
#             # limit this to 20 for now
#             queryset = Products.objects.all()[:20]
#             # paginator = Paginator(queryset, per_page=10)
#             serializer = ProductSerializer(queryset, many=True)
#             return Response(
#                 {
#                     "data": serializer.data,
#                     "message": "Products fetched successfully",
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except Exception as error:
#             print(error)
#             return Response(
#                 {
#                     "data": {},
#                     "message": "Sorry,something went wrong. Could not get the products.",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
