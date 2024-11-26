from rest_framework import serializers
from .models import Store, Category, Products


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    category_store = serializers.SlugRelatedField(
        slug_field="store_name", queryset=Store.objects.all()
    )

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"
