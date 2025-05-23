from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# 리스트 조회 + 새 상품 등록 (GET + POST)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# 단일 상품 수정/삭제 (PUT + DELETE)
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'productId'  # React에서 productId로 요청하기 때문
