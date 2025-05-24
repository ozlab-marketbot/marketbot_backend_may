# 예: api/fetch_naver_products.py

import requests
from django.conf import settings
from yourapp.models import Product  # 너의 앱과 모델명에 맞게 수정

def fetch_and_save_products():
    headers = {
        "Authorization": f"Bearer {settings.NAVER_API_ACCESS_TOKEN}"
    }
    response = requests.get("https://api.naver.com/your-endpoint", headers=headers)
    
    if response.status_code == 200:
        products = response.json().get("products", [])
        
        for p in products:
            Product.objects.update_or_create(
                product_id=p["id"],
                defaults={
                    "name": p["name"],
                    "price": p["price"],
                    "category": p["category"],
                    "image_url": p["image"],
                }
            )
    else:
        print("❌ 네이버 API 호출 실패:", response.status_code, response.text)
