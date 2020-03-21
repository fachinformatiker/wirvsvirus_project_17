from functools import wraps
from flask import request, abort
from control_service import app

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/market/<int:user_id>/get')
def get_market(id):
    return id

@app.route('/market/get')
def get_market_body():
    print(request)
    if(request.is_json == True and request.method == 'GET'):
        return request.json
    return {}
@app.route('/marketlist/')
def get_marketlist(id):
    return 'Hello World!'