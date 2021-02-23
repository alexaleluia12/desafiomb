import datetime

from flask import Flask, jsonify, request
from marshmallow import ValidationError

import database
from validation_shema import CoinSchema

app = Flask(__name__)

database.close_connection_cl(app)

@app.route('/<pair>/mms', methods=['GET'])
def get_avg(pair):
    data = None
    try:
        input_params = dict(request.args)
        input_params['pair'] = pair
        data = CoinSchema().load(input_params)
    except ValidationError as exc:
        return exc.messages, 400

    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day)
    past_one_year = today - datetime.timedelta(days=365)
    if data['from_'] < past_one_year.timestamp():
        return {'from': 'invalid value past then 365 days'}, 400

    if data.get('to', None) is None:
        data['to'] = (today - datetime.timedelta(1)).timestamp()

    cursor = database.get_db().cursor()

    cursor.execute(
        f'''SELECT "timestamp", mms_{data["range_"]} as mms
            FROM coins where pair = ? and "timestamp" >= {data["from_"]} and "timestamp" <= {data["to"]}
            ORDER BY timestamp ASC''',
        (data['pair'],)
    )
    result = cursor.fetchall()
    formated_result = []
    for element in result:
        formated_result.append({'timestamp': element['timestamp'], 'mms': round(element['mms'], 2)})
    return jsonify(formated_result)



app.run(debug=True, port=3001, host='0.0.0.0')