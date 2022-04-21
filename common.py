import requests
import json
import time
import configparser
import os.path
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


ACC_TOKEN_FILE_NAME = 'acc_token.json'
BASE_REST_URL = 'https://openapi.koreainvestment.com:9443'
BASE_WS_URL = 'ws://ops.koreainvestment.com:21000'


def get_keys(config_file_nm: str) -> tuple:
    if not os.path.exists(config_file_nm):
        return None, None

    cp = configparser.ConfigParser()
    cp.read(config_file_nm)
    app_key = cp['Key']['AppKey']
    app_secret = cp['Key']['AppSecret']

    return app_key, app_secret


def get_acc_token(app_key: str, app_secret: str) -> tuple:
    if os.path.exists(ACC_TOKEN_FILE_NAME):
        with open('acc_token.json', 'r', encoding='utf-8') as f:
            acc_token_info: dict = json.loads(f.read())
            expire_ts = int(acc_token_info.get('expire_ts', 0))

            if int(time.time()) < expire_ts:
                return acc_token_info.get('token_type'), acc_token_info.get('acc_token')

    req_url = f'{BASE_REST_URL}/oauth2/tokenP'

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


def get_hashkey(app_key: str, app_secret: str, data: dict) -> str:
    req_url = f'{BASE_REST_URL}/uapi/hashkey'

    req_header = {
        'content-type': 'application/json; charset=utf-8',
        'appkey': app_key,
        'appsecret': app_secret,
    }

    resp: dict = requests.post(url=req_url, headers=req_header, json=data).json()

    return resp.get('HASH')


def get_account_infos(config_file_nm: str) -> tuple:
    if not os.path.exists(config_file_nm):
        return None, None

    cp = configparser.ConfigParser()
    cp.read(config_file_nm)
    hts_id = cp['Account']['HtsId']
    acc_no = cp['Account']['AccNo']
    acc_cd = cp['Account']['AccCd']

    return hts_id, acc_no, acc_cd


def decrypt_str(cipher_str: str, key: str, iv: str) -> str:
    decryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, IV=iv.encode('utf-8'))
    return bytes.decode(unpad(decryptor.decrypt(base64.b64decode(cipher_str)), AES.block_size))
