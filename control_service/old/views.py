from flask import jsonify
from control_service import app,cache

@app.route('/')
@cache.cached(timeout=50)
def hello_world():
    return 'Hello World!'

@app.route('/static/markt/')
@cache.cached(timeout=50)
def get_marketstatic():
    print(id)
    market = {"marketid": 42, "Name": "TollerNetto", "Company": "aldi", "GPSlocation": {"lat": 42.1231, "long": 100.1},
              "Adresse": "Straße", "status": 1, "timestamp": "01-01-1970"}

    return jsonify(market)



