import requests
import json
import time
import os.path

ACC_TOKEN_FILE_NAME = 'acc_token.json'
BASE_URL = 'https://openapi.koreainvestment.com:9443'


def get_acc_token(app_key: str, app_secret: str) -> tuple:
    if os.path.exists(ACC_TOKEN_FILE_NAME):
        with open('acc_token.json', 'r', encoding='utf-8') as f:
            acc_token_info: dict = json.loads(f.read())
            expire_ts = int(acc_token_info.get('expire_ts', 0))

            if int(time.time()) < expire_ts:
                return acc_token_info.get('token_type'), acc_token_info.get('acc_token')

    req_url = f'{BASE_URL}/oauth2/tokenP'

    req_body = {
        'grant_type': 'client_credentials',
        'appkey': app_key,
        'appsecret': app_secret
    }

    resp: dict = requests.post(url=req_url, json=req_body).json()

    token_type: str = resp.get('token_type')
    expire_ts: int = int(time.time()) + resp.get('expires_in', 0)
    acc_token: str = resp.get('access_token')

    with open('acc_token.json', 'w', encoding='utf-8') as f:
        data = {
            'token_type': token_type,
            'acc_token': acc_token,
            'expire_ts': expire_ts
        }

        f.write(json.dumps(data))

    return token_type, acc_token
