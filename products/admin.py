from django.contrib import admin

# Register your models here.
from .models import Store, Category, Products


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["store_name", "store_base_url"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = []


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "product_name",
        "product_barcode",
        "product_price",
        "product_category",
        "product_weight",
        "product_store",
        "product_date",
        "product_url",
    ]
