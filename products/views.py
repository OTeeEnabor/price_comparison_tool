from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response

from .models import Products
from .serializers import ProductSerializer


# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 50


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
