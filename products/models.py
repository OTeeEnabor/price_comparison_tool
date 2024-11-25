from django.db import models


# Create your models here.
class Store(models.Model):
    store_name = models.CharField(max_length=250)
    store_base_url = models.CharField(max_length=320)

    def __str__(self):
        return f"{self.store_name}"


class Category(models.Model):
    category_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=300)
    category_url = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.category.store_name} - {self.category_name}"


class Products(models.Model):
    product_name = models.CharField(max_length=250)
    product_barcode = models.CharField(max_length=120)
    product_date = models.DateField()
    product_category = models.CharField(max_length=120)
    product_price = models.DecimalField(decimal_places=2, max_digits=8)
    product_weight = models.DecimalField(decimal_places=3, max_digits=8)
    product_url = models.CharField(max_length=320)
    product_store = models.CharField(max_length=120)

    class Meta:
        db_table = "products"
