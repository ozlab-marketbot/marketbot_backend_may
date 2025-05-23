from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):  # ✅ POST 허용
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):  # ✅ PUT/DELETE 허용
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'productId'  # ✅ 여기 핵심


#api 연동시 사용할 코드 
# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from .models import Product
# from .serializers import ProductSerializer

# NAVER_API_BASE = "https://api.commerce.naver.com"
# TOKEN_URL = "https://api.commerce.naver.com/auth/token"


# class NaverSyncView(APIView):
#     permission_classes = [AllowAny]

#     def get_token(self):
#         response = requests.post(
#             TOKEN_URL,
#             data={
#                 "client_id": settings.NAVER_CLIENT_ID,
#                 "client_secret": settings.NAVER_CLIENT_SECRET,
#                 "grant_type": "client_credentials"
#             },
#             headers={"Content-Type": "application/x-www-form-urlencoded"}
#         )
#         response.raise_for_status()
#         return response.json().get("access_token")

#     def get(self, request):
#         token = self.get_token()

#         # 네이버 채널 상품 조회
#         res = requests.get(
#             f"{NAVER_API_BASE}/v2/products/channel-products",
#             headers={"Authorization": f"Bearer {token}"}
#         )

#         if res.status_code != 200:
#             return JsonResponse({"error": "네이버 상품 가져오기 실패"}, status=500)

#         products = res.json().get("data", [])  # 실제 응답 형식에 따라 key 수정 필요

#         saved = []
#         for item in products:
#             obj, _ = Product.objects.update_or_create(
#                 productId=item.get("channelProductNo"),  # 네이버 고유 ID 사용
#                 defaults={
#                     "title": item.get("name"),
#                     "brand": item.get("brandName", ""),
#                     "maker": item.get("manufacturer", ""),
#                     "image": item.get("imageUrl", ""),
#                     "link": item.get("url", ""),
#                     "lprice": item.get("price", ""),
#                     "hprice": "",
#                     "mallName": item.get("saleSite", ""),
#                     "productType": str(item.get("productType", 1)),
#                     "category1": item.get("category1Name", ""),
#                     "category2": item.get("category2Name", ""),
#                     "category3": item.get("category3Name", ""),
#                     "category4": item.get("category4Name", ""),
#                 }
#             )
#             saved.append(obj.productId)

#         return JsonResponse({"synced": saved})
