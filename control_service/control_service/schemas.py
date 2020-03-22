from schema import Schema, And, SchemaError, Or
from flask import request, abort

SETMARKETSCHEMA = Schema({
    "MarketID": And(int, lambda i: i >= 0),
    "Status": Or(None, And(int, lambda s: 1 <= s and s <= 3))
})

REGISTERSCHEMA = Schema({
    "Username": And(str, lambda s: 1 <= len(s) and len(s) <= 20),
    "Password": And(str, lambda s: 1 <= len(s))  # TODO max length?
})
LOGINSCHEMA = REGISTERSCHEMA

PROFILESCHEMA = Schema({
    "Token": And(str, len)
})


def get_validated_json(validation_schema: Schema):
    """
    Returns the validated json of the requests according to the provided schema.

    Aborts with 400 on error.
    """
    if not request.is_json:
        abort(400)
    
    data = request.get_json()
    
    try:
        data = validation_schema.validate(data)
    except SchemaError:
        abort(400)

    return data
