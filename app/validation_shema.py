
from marshmallow import Schema, fields, validate

class CoinSchema(Schema):
    from_ = fields.Int(required=True, data_key='from')
    range_ = fields.Int(required=True, data_key='range', validate=validate.OneOf([20, 50, 200]))
    to = fields.Int(required=False)
    pair = fields.Str(required=True, validate=validate.OneOf(['BRLBTC', 'BRLETH']))

