import bcrypt
import pybase64
import time
import requests
import json
import http.client
from apikey import config

client_id = config["CLIENT_ID"]     
client_secret = config["CLIENT_SECRET"]

timestamp = int(time.time() * 1000)
password = client_id + "_" + str(timestamp)
hashed = bcrypt.hashpw(password.encode('utf-8'), client_secret.encode('utf-8'))
client_secret_sign = pybase64.standard_b64encode(hashed).decode('utf-8')

url = "https://api.commerce.naver.com/external/v1/oauth2/token"

data = {
    "client_id": client_id,
    "timestamp": timestamp,
    "client_secret_sign": client_secret_sign,
    "grant_type": "client_credentials",
    "type": "SELF"
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}
res = requests.post(url, data=data, headers=headers)
json_data = json.loads(res.text)
access_token = json_data['access_token']

# ----------- 채널 상품 조회 ------------
# 예시 URL: https://smartstore.naver.com/sportstoktok/products/7058693395
# "7058693395"는 원상품번호가 아닌 "채널상품번호"

channelProductNo = 7058693395
conn = http.client.HTTPSConnection("api.commerce.naver.com")

headers = {
    'Authorization': 'Bearer ' + str(access_token)
}

# 올바른 endpoint: /external/v2/products/channel-products/{channelProductNo}
conn.request("GET", f"/external/v2/products/channel-products/{channelProductNo}", headers=headers)
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))