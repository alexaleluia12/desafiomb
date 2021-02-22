import time
import datetime
import sqlite3
import traceback

import schedule
import requests

import const
from helpers import movin_average, store_coin

def update_currency(currency):
    try:
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        yesterday = today - datetime.timedelta(1)
        past = yesterday - datetime.timedelta(201)

        http_response = requests.get(const.URL_DATA.format(currency, int(past.timestamp()), int(yesterday.timestamp())))
        candles = http_response.json()['candles']
        movin_average(candles, 20)
        movin_average(candles, 50)
        movin_average(candles, 200)

        with sqlite3.connect(const.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            store_coin(currency, candles[-1: ], cursor)
            connection.commit()
        print(f'Update {currency} - ' + now.isoformat())

    except Exception as exc:
        print(f'Fail to update {currency}')
        print(exc)
        traceback.print_exc()

def job():
    for currency in [const.BITCOIN, const.ETHEREUM]:
        update_currency(currency)


def is_consecutive(data):
    for i in range(len(data) - 1):
        current = data[i]
        next_ = data[i+1]
        if (next_[0] - current[0]) < (60*60*24):
            return False
    return True

def verify_consistency():
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day)
    yesterday = today - datetime.timedelta(1)

    with sqlite3.connect(const.DATABASE_NAME) as connection:
        cursor = connection.cursor()
        for currency in [const.BITCOIN, const.ETHEREUM]:
            cursor.execute(f'''
                SELECT timestamp as ts
                FROM coins WHERE pair = ?
                ORDER BY ts
                DESC LIMIT 365''', (currency,)
            )
            data = cursor.fetchall()

            consecutive = is_consecutive(data)
            if not consecutive:
                print(f'Currency {currency} lost one value')


schedule.every().day.at("11:00").do(job)
schedule.every().day.at("12:10").do(verify_consistency)

while True:
    schedule.run_pending()
    time.sleep(1)