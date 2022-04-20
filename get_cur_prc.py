import common
import requests


def main(shtcode: str) -> None:
    app_key, app_secret = common.get_keys('config.ini')
    token_type, acc_token = common.get_acc_token(app_key, app_secret)

    req_header = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': f'{token_type} {acc_token}',
        'appkey': app_key,
        'appsecret': app_secret,
        'tr_id': 'FHKST01010100',
    }

    req_body = {
        'FID_COND_MRKT_DIV_CODE': 'J',
        'FID_INPUT_ISCD': shtcode,
    }

    path = '/uapi/domestic-stock/v1/quotations/inquire-price'
    req_url = f'{common.BASE_REST_URL}/{path}'

    resp = requests.get(req_url, headers=req_header, params=req_body)
    print(resp.text)


if '__main__' == __name__:
    main('005930')
