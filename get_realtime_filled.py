import common
import websocket
import json
import threading
import time


aes_key: str = ''
iv: str = ''


def subscribe(ws: websocket.WebSocketApp):
    app_key, app_secret = common.get_keys('config.ini')

    req = {
        'header': {
            'appkey': app_key,
            'appsecret': app_secret,
            'custtype': 'P',
            'tr_type': '1',
            'content-type': 'utf-8'},
        'body': {
            'input': {
                'tr_id': 'H0STCNI0',
                'tr_key': '',
            }
        }
    }

    ws.send(json.dumps(req))


def unsubscribe(ws: websocket.WebSocketApp):
    app_key, app_secret = common.get_keys('config.ini')

    req = {
        'header': {
            'appkey': app_key,
            'appsecret': app_secret,
            'custtype': 'P',
            'tr_type': '2',
            'content-type': 'utf-8'},
        'body': {
            'input': {
                'tr_id': 'H0STCNI0',
                'tr_key': '',
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
    first_str = msg[0]

    # json으로 처리를 해야할 경우
    if '0' != first_str and '1' != first_str:
        rcv: dict = json.loads(msg)
        trid = rcv['header']['tr_id']

        if 'PINGPONG' == trid:
            ws.send(msg)
        elif 'H0STCNI0' == trid:
            global aes_key
            global iv

            output = rcv['body']['output']
            aes_key = output['key']
            iv = output['iv']

        print(msg)
        return

    msgs = msg.split('|')
    data_cnt: int = int(msgs[2])
    raw_data: str = msgs[3]

    print(raw_data)

    # TODO: 복호화


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
