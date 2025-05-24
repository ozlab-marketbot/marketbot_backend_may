import bcrypt
import pybase64
import time
import requests
import json
import math
import csv
from apikey import config  # CLIENT_ID, CLIENT_SECRET 포함된 모듈

client_id = config["CLIENT_ID"]
client_secret = config["CLIENT_SECRET"]

# ---------- 1. 토큰 발급 ----------
timestamp = int(time.time() * 1000)
password = f"{client_id}_{timestamp}"
hashed = bcrypt.hashpw(password.encode('utf-8'), client_secret.encode('utf-8'))
client_secret_sign = pybase64.standard_b64encode(hashed).decode('utf-8')

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
access_token = token_json['access_token']
print("✅ Access token 발급 완료")

# ---------- 2. 전체 상품정보 수집 및 CSV 저장 ----------
page = 1
page_size = 100
print("🔍 전체 상품정보 수집 중...")

collected_products = []

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

    if res.status_code != 200:
        print(f"❌ 실패: {res.status_code}")
        print(res.text)
        break

    data = res.json()
    print("📥 응답 샘플:", json.dumps(data, indent=2, ensure_ascii=False))

    # 여기서 실제 응답 구조에 따라 products 추출
    products = data.get("contents", [])


    if not products:
        print("⚠️ products 리스트가 비어 있습니다.")
        break

    for product in products:
        origin_no = product.get("originProductNo")
        channel_products = product.get("channelProducts", [])

        for cp in channel_products:
            row = {
                "originProductNo": origin_no,
                "channelProductNo": cp.get("channelProductNo"),
                "name": cp.get("name"),
                "price": cp.get("salePrice"),
                "stock": cp.get("stockQuantity"),
                "status": cp.get("statusType")
            }
            collected_products.append(row)


    total_pages = data.get("totalPages") or data.get("data", {}).get("totalPages", 1)
    print(f"📄 Page {page}/{total_pages} 수집 완료")
    if page >= total_pages:
        break
    page += 1

# ---------- 3. CSV 저장 ----------
if collected_products:
    with open("products_output.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
        fieldnames = ["originProductNo", "channelProductNo", "name", "price", "stock", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(collected_products)
    print(f"📁 CSV 저장 완료: products_output.csv ({len(collected_products)}개)")
else:
    print("⚠️ 저장할 상품 데이터가 없습니다.")

    print("응답 키 목록:", data.keys())
print("예상되는 리스트 형태의 키 예시:", type(data.get("products")), type(data.get("content")))

