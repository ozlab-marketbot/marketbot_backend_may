# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreProductViewSet, fetch_storefarm_products

router = DefaultRouter()
router.register(r'', StoreProductViewSet, basename='products')

urlpatterns = [
    path('sync/', fetch_storefarm_products),  # 동기화용
    path('', include(router.urls)),
]
