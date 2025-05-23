from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    brand = models.CharField(max_length=100)
    maker = models.CharField(max_length=100)
    title = models.TextField()
    image = models.URLField()
    link = models.URLField()
    lprice = models.CharField(max_length=20)
    hprice = models.CharField(max_length=20, blank=True)
    mallName = models.CharField(max_length=255)
    productId = models.CharField(max_length=50, unique=True)
    productType = models.CharField(max_length=10)
    category1 = models.CharField(max_length=100, blank=True)
    category2 = models.CharField(max_length=100, blank=True)
    category3 = models.CharField(max_length=100, blank=True)
    category4 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"[{self.brand}] {self.title[:30]}"
