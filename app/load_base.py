import requests
import datetime
import sqlite3

import const
from helpers import movin_average, store_coin


def request_candles(currency):
    now = datetime.datetime.now()

    past = now - datetime.timedelta(days=365+201)
    response = requests.get(const.URL_DATA.format(currency, int(past.timestamp()), int(now.timestamp())))
    json_response = response.json()
    return json_response['candles']


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
