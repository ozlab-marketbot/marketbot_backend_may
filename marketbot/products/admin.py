from django.contrib import admin  # ✅ 이 줄을 꼭 추가해야 함
from .models import StoreProduct

@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('channel_product_no', 'name', 'price', 'stock', 'status')
