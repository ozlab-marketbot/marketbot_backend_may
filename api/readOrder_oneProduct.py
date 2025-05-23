import bcrypt
import pybase64
import time
import requests
import json
import math
import http.client
from apikey import config  # CLIENT_ID, CLIENT_SECRET 포함된 모듈

# ---------- 1. 토큰 발급 ----------
client_id = config["CLIENT_ID"]
client_secret = config["CLIENT_SECRET"]  # bcrypt 해시 형식이어야 함 (e.g., $2a$...)

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

# ---------- 2. 단일 채널 상품 조회 ----------
channelProductNo = 11815327167
conn = http.client.HTTPSConnection("api.commerce.naver.com")

headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

conn.request("GET", f"/external/v2/products/channel-products/{channelProductNo}", headers=headers)
res = conn.getresponse()
data = res.read()

print("Status:", res.status)
print("Response:", data.decode("utf-8"))