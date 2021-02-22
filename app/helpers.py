

def movin_average(lst, period):
    max_ = len(lst)
    for i in range(max_):
        if i - period + 1 < 0:
            continue
        sublist = lst[i - period + 1: i + 1]
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