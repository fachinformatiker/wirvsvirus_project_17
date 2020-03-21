from functools import wraps
from flask import jsonify
from flask import request, abort
from control_service import app

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/market/getbyid/<int:id>')
def get_market(id):
    print(id)
    market = {"marketid": 42, "Name": "TollerNetto", "Company": "aldi", "GPSlocation": {"lat": 42.1231, "long": 100.1},
              "Adresse": "Straße", "status": 1, "timestamp": "01-01-1970"}

    return jsonify(market)

@app.route('/market/get')
def get_market_body():
    #help needed
    if(request.method == 'GET'):
        market={"marketid":42,"Name":"TollerNetto","Company":"aldi","GPSlocation":{"lat":42.1231,"long":100.1},"Adresse":"Straße","status":1,"timestamp":"01-01-1970"}
        return jsonify(market)
    abort(400)

@app.route('/marketlist/<float:lat>/<float:long>/')
def get_marketlist(lat,long):
    if (request.method == 'GET'):
        marketlist={"Markets":[{"marketid":42,"Name":"TollerNetto","Company":"aldi","GPSlocation":{"lat":42.1231,"long":100.1},"Adresse":"Straße","status":1,"timestamp":"01-01-1970"}]}
        return jsonify(marketlist)
    abort(400)