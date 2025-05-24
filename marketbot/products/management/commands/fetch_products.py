import time
import bcrypt
import pybase64
import requests
import json

from django.core.management.base import BaseCommand
from products.models import StoreProduct
from apikey import config # ← apikey.py는 marketbot 폴더에 있어야 함

class Command(BaseCommand):
    help = '네이버 스마트스토어 API에서 상품 데이터를 가져와 StoreProduct 모델에 저장합니다.'

    def handle(self, *args, **kwargs):
        client_id = config["CLIENT_ID"]
        client_secret = config["CLIENT_SECRET"]

        timestamp = int(time.time() * 1000)
        password = f"{client_id}_{timestamp}"
        hashed = bcrypt.hashpw(password.encode('utf-8'), client_secret.encode('utf-8'))
        client_secret_sign = pybase64.standard_b64encode(hashed).decode('utf-8')

        # 1. 토큰 요청
        token_url = "https://api.commerce.naver.com/external/v1/oauth2/token"
        data = {
            "client_id": client_id,
            "timestamp": timestamp,
            "client_secret_sign": client_secret_sign,
            "type": "SELF"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        token_response = requests.post(token_url, data=data, headers=headers)
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        if not access_token:
            self.stdout.write(self.style.ERROR("❌ 토큰 발급 실패"))
            return

        self.stdout.write(self.style.SUCCESS("✅ Access token 발급 완료"))

        # 2. 상품 요청
        page = 1
        page_size = 100
        collected = 0

        while True:
            payload = {"page": page, "size": page_size}
            res = requests.post(
                "https://api.commerce.naver.com/external/v1/products/search",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                data=json.dumps(payload)
            )

            if res.status_code != 200:
                self.stdout.write(self.style.ERROR(f"❌ 상품 요청 실패: {res.status_code}"))
                self.stdout.write(res.text)
                break

            data = res.json()
            products = data.get("contents", [])

            if not products:
                self.stdout.write("⚠️ products 리스트가 비어 있음. 종료.")
                break

            for product in products:
                origin_no = product.get("originProductNo")
                channel_products = product.get("channelProducts", [])

                for cp in channel_products:
                    StoreProduct.objects.update_or_create(
                        channel_product_no=cp.get("channelProductNo"),
                        defaults={
                            "origin_product_no": origin_no,
                            "name": cp.get("name"),
                            "price": cp.get("salePrice"),
                            "stock": cp.get("stockQuantity"),
                            "status": cp.get("statusType"),
                        }
                    )
                    collected += 1

            total_pages = data.get("totalPages", 1)
            self.stdout.write(f"📄 Page {page}/{total_pages} 수집 완료")
            if page >= total_pages:
                break
            page += 1

        self.stdout.write(self.style.SUCCESS(f"🎉 총 {collected}개 상품 저장 완료"))
