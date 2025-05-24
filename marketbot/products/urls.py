from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreProductViewSet, fetch_storefarm_products

router = DefaultRouter()
router.register(r'', StoreProductViewSet)  # /api/products/ 로 전체 StoreProduct 목록 반환

urlpatterns = [
    path('sync/', fetch_storefarm_products),  # 이건 /api/products/sync/로 네이버 API 연동
    path('', include(router.urls)),           # 이건 /api/products/로 전체 리스트 반환
]
