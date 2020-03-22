from functools import wraps
from flask import request, abort, jsonify
import jwt
from control_service import app, auth, db,cache
from control_service.models import UserData, Stammdaten
from control_service.schemas import SETMARKETSCHEMA
from schema import SchemaError

@app.route('/market/<int:id>', methods=['GET'])
@cache.cached(timeout=50)
def get_market(id):
    return jsonify(db.session.query(Stammdaten).filter_by(id=id).first())


"""
@app.route('/market/get')
def get_market_body():
    if(request.method == 'GET'):
        market=db.session.query(Stammdaten).filter_by(id=id).first()
        return jsonify(market)
    abort(400)
"""
@app.route('/marketlist/', methods=['GET'])
@cache.cached(timeout=50)
def get_marketlist():
    return jsonify(db.session.query(Stammdaten).all())


@app.route('/market/', methods=['PUT'])
def set_market():
    """
    Endpoint: /market/
    Methods:  PUT
    Parameter: MarketID - id of the market
               Status   - the Status the status of the market should change to

    The function takes a json object with the key/value pairs descripted by Parameters and 
    initiates the corresponding db change.
    """
    if request.is_json == True:
        content = request.get_json()  # TODO: validation

        try:
            content = SETMARKETSCHEMA.validate(content)
        except SchemaError:
            abort(400)

        success = update_market_status(content['MarketID'], content['Status'])
        return jsonify({"Success": success})
    else:
        abort(400)

@app.route('/market/', methods=['POST'])
def create_market():
    """
    Endpoint: /market/
    Methods:  POST
    Parameter:
    """
    print(request.is_json)
    if request.is_json:
        print("sucess")
        content = request.get_json()  # TODO: validation
        print("hi")
        """
        try:
            content = SETMARKETSCHEMA.validate(content)
        except SchemaError:
            abort(400)
        """
        print(content)
        success = create_market_entity(content['MarketID'], content['Name'],content["Company"],content["GPSLocation"]["Lat"],content["GPSLocation"]["Long"],content["Adresse"],content["Enabled"],content["Status"])
        return jsonify({"Success": success})
    else:
        abort(400)

def update_market_status(market_id, status): 
    """
    :param market_id: market_id - id of the market
                      status    - the Status the status of the market should change to

    This function updated the status of the market in the db. The timestamp is automatically updated.
    """
    market = db.session.query(Stammdaten).filter_by(id=market_id).first()
    
    if market == None:
        return False
    
    market.status = status
    db.session.commit()
    return True

def create_market_entity(market_id,name,company,lat,long,adress,enabled,status):
    print(market_id,name,company,lat,long,enabled,status)
    market = Stammdaten(id=market_id, name=name, company=company, lat=lat, long=long,adresse=adress, enabled=enabled, status=status)
    if market == None:
        return False

    db.session.add(market)
    db.session.commit()
    return True
