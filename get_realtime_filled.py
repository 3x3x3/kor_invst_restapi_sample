import common
import websocket
import json
import threading
import time


FILLED_EVT_TR_ID = 'H0STCNI0'
aes_key: str = ''
iv: str = ''


def subscribe(ws: websocket.WebSocketApp):
    app_key, app_secret = common.get_keys('config.ini')
    hts_id, _, _ = common.get_account_infos('config.ini')

    req = {
        'header': {
            'appkey': app_key,
            'appsecret': app_secret,
            'custtype': 'P',
            'tr_type': '1',
            'content-type': 'utf-8'
        },
        'body': {
            'input': {
                'tr_id': FILLED_EVT_TR_ID,
                'tr_key': hts_id,
            }
        }
    }

    ws.send(json.dumps(req))


def unsubscribe(ws: websocket.WebSocketApp):
    app_key, app_secret = common.get_keys('config.ini')
    hts_id, _, _ = common.get_account_infos('config.ini')

    req = {
        'header': {
            'appkey': app_key,
            'appsecret': app_secret,
            'custtype': 'P',
            'tr_type': '2',
            'content-type': 'utf-8'
        },
        'body': {
            'input': {
                'tr_id': FILLED_EVT_TR_ID,
                'tr_key': hts_id,
            }
        }
    }

    ws.send(json.dumps(req))


def wait_close(ws: websocket.WebSocketApp):
    # 30초간 수신
    time.sleep(30)
    unsubscribe(ws)
    time.sleep(1)
    ws.close()


def on_message(ws: websocket.WebSocketApp, msg: str):
    global aes_key
    global iv

    first_str = msg[0]

    # json으로 처리를 해야할 경우
    if '0' != first_str and '1' != first_str:
        rcv: dict = json.loads(msg)
        trid = rcv['header']['tr_id']

        if 'PINGPONG' == trid:
            ws.send(msg)
        elif FILLED_EVT_TR_ID == trid:
            output = rcv['body']['output']
            aes_key = output['key']
            iv = output['iv']

        print(msg)
        return

    msgs = msg.split('|')
    data_cnt: int = int(msgs[2])
    raw_data: str = msgs[3]
    plain_data = common.decrypt_str(raw_data, aes_key, iv)

    datas = plain_data.split('^')

    for i in range(data_cnt):
        offset = 23 * i

        rcv = {
            '고객 ID': datas[0 + offset],
            '계좌번호': datas[1 + offset],
            '주문번호': datas[2 + offset],
            '원주문번호': datas[3 + offset],
            '매도매수구분': datas[4 + offset],
            '정정구분': datas[5 + offset],
            '주문종류': datas[6 + offset],
            '주문조건': datas[7 + offset],
            '주식 단축 종목코드': datas[8 + offset],
            '체결 수량': datas[9 + offset],
            '체결단가': datas[10 + offset],
            '주식 체결 시간': datas[11 + offset],
            '거부여부': datas[12 + offset],
            '체결여부': datas[13 + offset],
            '접수여부': datas[14 + offset],
            '지점번호': datas[15 + offset],
            '주문수량': datas[16 + offset],
            '계좌명': datas[17 + offset],
            '체결종목명': datas[18 + offset],
            '신용구분': datas[19 + offset],
            '신용대출일자': datas[20 + offset],
            '체결종목명40': datas[21 + offset],
            '주문가격': datas[22 + offset],
        }

        print(rcv)


def on_error(ws: websocket.WebSocketApp, error: str):
    print(error)


def on_close(ws: websocket.WebSocketApp, close_status_code, close_msg):
    print('### closed ###')


def on_open(ws: websocket.WebSocketApp):
    print('Opened connection')

    subscribe(ws)

    # 30초후 종료
    thd = threading.Thread(target=wait_close, args=(ws,), daemon=True)
    thd.start()


if __name__ == '__main__':
    websocket.enableTrace(True)
    websocket = websocket.WebSocketApp(common.BASE_WS_URL, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)

    websocket.run_forever()
