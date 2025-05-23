import time
import bcrypt
import base64
import requests
import urllib.parse
from apikey import config

client_id = config["CLIENT_ID"]
client_secret = config["CLIENT_SECRET"]

# 현재 시각 (밀리초)
timestamp = str(int(time.time() * 1000))

# bcrypt 해싱을 위한 비밀번호 생성: client_id + "_" + timestamp
password = f"{client_id}_{timestamp}".encode('utf-8')
salt = client_secret.encode('utf-8')

# bcrypt 해싱 후 base64 인코딩
hashed = bcrypt.hashpw(password, salt)
client_secret_sign = base64.b64encode(hashed).decode('utf-8')

# 인증 요청 payload
payload = {
    'client_id': client_id,
    'timestamp': timestamp,
    'client_secret_sign': client_secret_sign,
    'type': 'SELF'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}

# 인증 토큰 요청
response = requests.post(
    'https://api.commerce.naver.com/external/v1/oauth2/token',
    headers=headers,
    data=urllib.parse.urlencode(payload)
)

# 응답 출력
print("Status:", response.status_code)
print("Response:", response.text)
