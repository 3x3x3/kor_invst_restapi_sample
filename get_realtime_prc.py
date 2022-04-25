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
                'tr_id': 'H0STCNT0',
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
                'tr_id': 'H0STCNT0',
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
        offset = 46 * i

        rcv = {
            '유가증권단축종목코드': datas[0 + offset],
            '주식체결시간': datas[1 + offset],
            '주식현재가': datas[2 + offset],
            '전일대비부호': datas[3 + offset],
            '전일대비': datas[4 + offset],
            '전일대비율': datas[5 + offset],
            '가중평균주식가격': datas[6 + offset],
            '주식시가': datas[7 + offset],
            '주식최고가': datas[8 + offset],
            '주식최저가': datas[9 + offset],
            '매도호가1': datas[10 + offset],
            '매수호가1': datas[11 + offset],
            '체결거래량': datas[12 + offset],
            '누적거래량': datas[13 + offset],
            '누적거래대금': datas[14 + offset],
            '매도체결건수': datas[15 + offset],
            '매수체결건수': datas[16 + offset],
            '순매수 체결건수': datas[17 + offset],
            '체결강도': datas[18 + offset],
            '총 매도수량': datas[19 + offset],
            '총 매수수량': datas[20 + offset],
            '체결구분': datas[21 + offset],
            '매수비율': datas[22 + offset],
            '전일 거래량대비등락율': datas[23 + offset],
            '시가시간': datas[24 + offset],
            '시가대비 구분': datas[25 + offset],
            '시가대비': datas[26 + offset],
            '최고가 시간': datas[27 + offset],
            '고가대비구분': datas[28 + offset],
            '고가대비': datas[29 + offset],
            '최저가시간': datas[30 + offset],
            '저가대비구분': datas[31 + offset],
            '저가대비': datas[32 + offset],
            '영업일자': datas[33 + offset],
            '신 장운영 구분코드': datas[34 + offset],
            '거래정지 여부': datas[35 + offset],
            '매도호가잔량': datas[36 + offset],
            '매수호가잔량': datas[37 + offset],
            '총 매도호가잔량': datas[38 + offset],
            '총 매수호가잔량': datas[39 + offset],
            '거래량 회전율': datas[40 + offset],
            '전일 동시간 누적거래량': datas[41 + offset],
            '전일 동시간 누적거래량 비율': datas[42 + offset],
            '시간구분코드': datas[43 + offset],
            '임의종료구분코드': datas[44 + offset],
            '정적VI발동기준가': datas[45 + offset],
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
