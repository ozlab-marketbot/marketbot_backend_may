import requests
import json
from apikey import config

access_token = config["ACCESS_TOKEN"]
url = "https://api.commerce.naver.com/external/v1/products/search"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json;charset=UTF-8',
    'Authorization': f'Bearer {access_token}'
}

all_products = []
page = 1
while True:
    payload = {
        "page": page,
        "size": 100
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()
    products = data.get("data", {}).get("products", [])
    if not products:
        break
    all_products.extend(products)
    print(f"📦 Page {page}: {len(products)}개 상품 불러옴")
    page += 1

print(f"\n✅ 전체 상품 개수: {len(all_products)}개")
