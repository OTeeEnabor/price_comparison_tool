from django.contrib import admin

# Register your models here.
from .models import Products


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
