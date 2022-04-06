import configparser
import common
import requests


def main():
    shtcode = '005930'

    cp = configparser.ConfigParser()
    cp.read('config.ini')
    app_key = cp['Key']['AppKey']
    app_secret = cp['Key']['AppSecret']

    token_type, acc_token = common.get_acc_token(app_key, app_secret)

    base_url = 'https://openapi.koreainvestment.com:9443'
    path = '/uapi/domestic-stock/v1/quotations/inquire-price'

    req_header = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': f'{token_type} {acc_token}',
        'appkey': app_key,
        'appsecret': app_secret,
        'tr_id': 'FHKST01010100',
    }

    req_url = f'{base_url}/{path}?FID_COND_MRKT_DIV_CODE=J&FID_INPUT_ISCD={shtcode}'

    resp = requests.get(req_url, headers=req_header)
    print(resp.text)


if '__main__' == __name__:
    main()
