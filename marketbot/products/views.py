import time
import bcrypt
import pybase64
import requests
import json

from django.http import JsonResponse
from rest_framework import viewsets
from .models import StoreProduct
from .serializers import StoreProductSerializer  # serializers.py에 있어야 함
from apikey import config


class StoreProductViewSet(viewsets.ModelViewSet):
    queryset = StoreProduct.objects.all().order_by('-id')
    serializer_class = StoreProductSerializer


def fetch_storefarm_products(request):
    try:
        client_id = config["CLIENT_ID"]
        client_secret = config["CLIENT_SECRET"]
        timestamp = int(time.time() * 1000)
        password = f"{client_id}_{timestamp}"
        hashed = bcrypt.hashpw(password.encode('utf-8'), client_secret.encode('utf-8'))
        client_secret_sign = pybase64.standard_b64encode(hashed).decode('utf-8')

        token_res = requests.post(
            "https://api.commerce.naver.com/external/v1/oauth2/token",
            data={
                "client_id": client_id,
                "timestamp": timestamp,
                "client_secret_sign": client_secret_sign,
                "type": "SELF"
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
        )

        token_json = token_res.json()
        access_token = token_json.get("access_token")
        if not access_token:
            return JsonResponse({"error": "토큰 발급 실패", "detail": token_json}, status=500)

        saved = 0
        page = 1
        page_size = 100

        while True:
            payload = {
                "page": page,
                "size": page_size
            }

            res = requests.post(
                "https://api.commerce.naver.com/external/v1/products/search",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                data=json.dumps(payload)
            )

            print("🛍️ 응답코드:", res.status_code)
            if res.status_code != 200:
                print("❌ 응답 오류:", res.text)
                break

            data = res.json()
            contents = data.get("contents", [])
            if not contents:
                print("⚠️ contents 없음, 종료")
                break

            for product in contents:
                origin_no = product.get("originProductNo")
                channel_products = product.get("channelProducts", [])
                for cp in channel_products:
                    pid = cp.get("channelProductNo")
                    name = cp.get("name", "")
                    price = cp.get("salePrice", "")
                    stock = cp.get("stockQuantity", "")
                    status = cp.get("statusType", "")

                    print(f"▶ 저장: {pid} | {name} | {price}")

                    StoreProduct.objects.update_or_create(
                        channel_product_no=pid,
                        defaults={
                            "origin_product_no": origin_no,
                            "name": name,
                            "price": price,
                            "stock": stock,
                            "status": status
                        }
                    )
                    saved += 1

            total_pages = data.get("totalPages", 1)
            if page >= total_pages:
                break
            page += 1

        return JsonResponse({"result": "성공", "saved": saved})

    except Exception as e:
        print("❌ 예외:", str(e))
        return JsonResponse({"error": "서버 오류", "detail": str(e)}, status=500)
