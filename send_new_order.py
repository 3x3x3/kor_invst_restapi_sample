import common
import requests


def main(tr_id: str, shtcode: str, qty: int, prc: int) -> None:
    app_key, app_secret = common.get_keys('config.ini')
    _, acc_no, acc_cd = common.get_account_infos('config.ini')
    token_type, acc_token = common.get_acc_token(app_key, app_secret)

    req_body = {
        'CANO': acc_no,
        'ACNT_PRDT_CD': acc_cd,
        'PDNO': shtcode,
        'ORD_DVSN': '00',
        'ORD_QTY': str(qty),
        'ORD_UNPR': str(prc),
    }

    hashkey = common.get_hashkey(app_key, app_secret, req_body)

    req_header = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': f'{token_type} {acc_token}',
        'appkey': app_key,
        'appsecret': app_secret,
        'tr_id': tr_id,
        'hashkey': hashkey,
    }

    path = '/uapi/domestic-stock/v1/trading/order-cash'
    req_url = f'{common.BASE_REST_URL}/{path}'

    resp = requests.post(req_url, headers=req_header, json=req_body).json()
    print(resp)


if '__main__' == __name__:
    # tr_id 구분값
    # TTTC0802U: 매수
    # TTTC0801U: 매도
    main('TTTC0802U', '005930', 1, 66000)
