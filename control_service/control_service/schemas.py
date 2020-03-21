from schema import Schema, And, Optional

SETMARKETSCHEMA = Schema({
    "MarketID": And(int, lambda i: i >= 0),
    "Status": Optional(And(int, lambda s: 1 <= s and s <= 3))
})
