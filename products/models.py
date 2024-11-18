from django.db import models

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=250)
    product_barcode = models.CharField(max_length=120)
    product_date = models.DateField()
    product_category = models.CharField(max_length=120)
    product_price = models.DecimalField(decimal_places=2,max_digits=8)
    product_weight = models.DecimalField(decimal_places=3,max_digits=8)
    product_url = models.CharField(max_length=320)
    product_store = models.CharField(max_length=120)

    class Meta:
        db_table = "products"