import requests
import datetime
import sqlite3

import const


def request_candles(currency):
    url_template = 'https://mobile.mercadobitcoin.com.br/v4/{}/candle?from={}&to={}&precision=1d'
    now = datetime.datetime.now()

    past = now - datetime.timedelta(days=365+200)

    response = requests.get(url_template.format(currency, int(past.timestamp()), int(now.timestamp())))
    json_response = response.json()
    return json_response['candles']

def movin_average(lst, period):
    max_ = len(lst)
    mv = []
    for i in range(max_-1, period-1, -1):
        sublist = lst[i - period: i]
        sum_ = 0.0
        for j in sublist:
            sum_ += j['close']
        lst[i]['ma_'+str(period)] = sum_/period

def store_coin(coin_name, coins, db_cursor):
    for coin in coins:
        db_cursor.execute(f"""INSERT INTO coins VALUES
            ('{coin_name}', {coin['timestamp']}, {coin['ma_20']},
            {coin['ma_50']}, {coin['ma_200']})"""
        )

ethereum = request_candles(const.ETHEREUM)
print('Download ethereum')
movin_average(ethereum, 20)
movin_average(ethereum, 50)
movin_average(ethereum, 200)

btc = request_candles(const.BITCOIN)
print('Download bitcoin')
movin_average(btc, 20)
movin_average(btc, 50)
movin_average(btc, 200)

with sqlite3.connect(const.DATABASE_NAME) as connection:
    cursor = connection.cursor()

    sql_template = '''
        CREATE TABLE coins (pair text, timestamp int, mms_20 real, mms_50 real, mms_200 real)
    '''
    cursor.execute(sql_template)
    store_coin(const.ETHEREUM, ethereum[-365: ], cursor)
    print('Store ethereum')

    store_coin(const.BITCOIN, btc[-365: ], cursor)
    print('Store bitcoin')

    connection.commit()

print('Finish load database')
