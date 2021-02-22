

def movin_average(lst, period):
    max_ = len(lst)
    for i in range(max_-1, period - 1, -1):
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