from django.db import models  # ← 반드시 있어야 함

class StoreProduct(models.Model):
    origin_product_no = models.CharField(max_length=50)
    channel_product_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    stock = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
