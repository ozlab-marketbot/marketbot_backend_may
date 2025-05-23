from django.urls import path
from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView

urlpatterns = [
    path('products/', ProductListCreateView.as_view()),
    path('products/<str:productId>/', ProductRetrieveUpdateDestroyView.as_view()),
]
