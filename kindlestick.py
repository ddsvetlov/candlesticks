#!/usr/bin/env python
from datetime import datetime
import json
import logging
import websocket


BASE_URL = 'wss://stream.binance.com:9443/ws'
MILLISECCONDS = 1000
TOKEN_PAIRS = ["ethusdt", "btcusdt", "bnbbtc"]


logging.basicConfig(filename="avg.log", level=logging.INFO)


def generate_stream_url(base_url, token_pairs):
    url = base_url
    for token in token_pairs:
        url+=f'/{token}@kline_1m'
    return url


def calculate_avg(price_list):
    if len(price_list) != 0:
        return sum(price_list) / len(price_list)
    else:
        return 0


def beauty_log(data, minute_price, avg):
    logs = f"Avg for pair {data.get('pair')} on time "\
           f"{datetime.fromtimestamp(minute_price[data.get('pair')]['start_time'] / MILLISECCONDS)}"\
           f" is: {avg}"
    logging.info(logs)
    print(logs)


def update_localstorage(data):

    if data.get('start_time')>minute_price[data.get('pair')].get('start_time'):
        avg = calculate_avg(minute_price[data.get('pair')].get('close_price'))
        beauty_log(data = data, minute_price=minute_price, avg=avg)
        minute_price[data.get('pair')].get('close_price').clear()
        minute_price[data.get('pair')]['start_time'] = data.get('close_time')
        minute_price[data.get('pair')].get('close_price').append(data.get('close_price'))   
    else:
        minute_price[data.get('pair')].get('close_price').append(data.get('close_price'))


def on_message(wsapp, message):
    message = json.loads(message)

    data = dict(
        pair = message.get('s'),
        start_time=message.get('k').get('t'),
        close_time=message.get('k').get('T'),
        close_price=float(message.get('k').get('c')),
    )
    if data.get('pair').lower() not in TOKEN_PAIRS:
        logging.info(f"Pair {pair} doesn't supported.")
    update_localstorage(data=data)


def on_error(wsapp, err):
    print("Got a an error: ", err)


def generate_ws_app_test(base_url, token_pairs):
    return websocket.WebSocketApp(
    generate_stream_url(base_url=base_url, token_pairs=token_pairs),
    header={"method":"SUBSCRIBE"}, 
    on_message=on_message,
    on_error=on_error,
)


if __name__ == "__main__":
    minute_price = {
        'ETHUSDT': {
            'start_time': 0, 
            'close_price': []
        }, 
        'BTCUSDT': {
            'start_time': 0, 
            'close_price': []
        }, 
        'BNBBTC': {
            'start_time': 0, 
            'close_price': []
        }
    }
    connection = generate_ws_app_test(base_url=BASE_URL, token_pairs=TOKEN_PAIRS)
    connection.run_forever()
