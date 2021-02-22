
from app.helpers import movin_average, store_coin


def test_movin_average():
    data = [
        {'close': 5}, {'close': 5}, {'close': 6.5}
    ]
    movin_average(data, 2)
    assert data[-1]['ma_2'] == 5.75