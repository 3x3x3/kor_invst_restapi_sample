import common
import websocket
import json
import threading
import time


def subscribe(ws: websocket.WebSocketApp, shtcode: str):
    app_key, app_secret = common.get_keys('config.ini')

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
                'tr_id': 'H0STASP0',
                'tr_key': shtcode,
            }
        }
    }

    ws.send(json.dumps(req))


def unsubscribe(ws: websocket.WebSocketApp, shtcode):
    app_key, app_secret = common.get_keys('config.ini')

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
                'tr_id': 'H0STASP0',
                'tr_key': shtcode,
            }
        }
    }

    ws.send(json.dumps(req))


def wait_close(ws: websocket.WebSocketApp):
    # 30초간 수신
    time.sleep(30)
    unsubscribe(ws, '005930')
    time.sleep(1)
    ws.close()


def on_message(ws: websocket.WebSocketApp, msg: str):
    first_str = msg[0]

    # json으로 처리를 해야할 경우
    if '0' != first_str and '1' != first_str:
        rcv: dict = json.loads(msg)
        trid = rcv['header']['tr_id']

        if 'PINGPONG' == trid:
            ws.send(msg)

        print(msg)
        return

    msgs = msg.split('|')
    data_cnt: int = int(msgs[2])
    raw_data: str = msgs[3]

    datas = raw_data.split('^')

    for i in range(data_cnt):
        offset = 52 * i

        rcv = {
            '유가증권 단축 종목코드': datas[0 + offset],
            '영업 시간': datas[1 + offset],
            '시간 구분 코드': datas[2 + offset],
            '매도호가1': datas[3 + offset],
            '매도호가2': datas[4 + offset],
            '매도호가3': datas[5 + offset],
            '매도호가4': datas[6 + offset],
            '매도호가5': datas[7 + offset],
            '매도호가6': datas[8 + offset],
            '매도호가7': datas[9 + offset],
            '매도호가8': datas[10 + offset],
            '매도호가9': datas[11 + offset],
            '매도호가10': datas[12 + offset],
            '매수호가1': datas[13 + offset],
            '매수호가2': datas[14 + offset],
            '매수호가3': datas[15 + offset],
            '매수호가4': datas[16 + offset],
            '매수호가5': datas[17 + offset],
            '매수호가6': datas[18 + offset],
            '매수호가7': datas[19 + offset],
            '매수호가8': datas[20 + offset],
            '매수호가9': datas[21 + offset],
            '매수호가10': datas[22 + offset],
            '매도호가 잔량1': datas[23 + offset],
            '매도호가 잔량2': datas[24 + offset],
            '매도호가 잔량3': datas[25 + offset],
            '매도호가 잔량4': datas[26 + offset],
            '매도호가 잔량5': datas[27 + offset],
            '매도호가 잔량6': datas[28 + offset],
            '매도호가 잔량7': datas[29 + offset],
            '매도호가 잔량8': datas[30 + offset],
            '매도호가 잔량9': datas[31 + offset],
            '매도호가 잔량10': datas[32 + offset],
            '매수호가 잔량1': datas[33 + offset],
            '매수호가 잔량2': datas[34 + offset],
            '매수호가 잔량3': datas[35 + offset],
            '매수호가 잔량4': datas[36 + offset],
            '매수호가 잔량5': datas[37 + offset],
            '매수호가 잔량6': datas[38 + offset],
            '매수호가 잔량7': datas[39 + offset],
            '매수호가 잔량8': datas[40 + offset],
            '매수호가 잔량9': datas[41 + offset],
            '매수호가 잔량10': datas[42 + offset],
            '총 매도호가 잔량': datas[43 + offset],
            '총 매수호가 잔량': datas[44 + offset],
            '시간외 총 매도호가 잔량': datas[45 + offset],
            '시간외 총 매수호가 잔량': datas[46 + offset],
            '예상 체결가': datas[47 + offset],
            '예상 체결량': datas[48 + offset],
            '예상 거래량': datas[49 + offset],
            '예상 체결 대비': datas[50 + offset],
            '예상 체결 대비 부호': datas[51 + offset],
        }

        print(rcv)


def on_error(ws: websocket.WebSocketApp, error: str):
    print(error)


def on_close(ws: websocket.WebSocketApp, close_status_code, close_msg):
    print('### closed ###')


def on_open(ws: websocket.WebSocketApp):
    print('Opened connection')

    subscribe(ws, '005930')

    # 30초후 종료
    thd = threading.Thread(target=wait_close, args=(ws,), daemon=True)
    thd.start()


if __name__ == '__main__':
    websocket.enableTrace(True)
    websocket = websocket.WebSocketApp(common.BASE_WS_URL, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)

    websocket.run_forever()
