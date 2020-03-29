from fastapi import APIRouter
from functools import wraps
from typing import List
from control_service.models import UserData, Stammdaten, sql_userdata, sql_stammdaten,database
from control_service.schemas import SETMARKETSCHEMA, get_validated_json
from control_service.jsonhelper import market_to_obj
# from flask import request, abort, jsonify
# import jwt
# from control_service import app, auth, db, cache

router = APIRouter()


@router.get('/')
def hello_world():
    return 'Hello World!'


@router.get('/static/markt/')
def get_marketstatic():
    print(id)
    market = {
        "marketid": 42,
        "Name": "TollerNetto",
        "Company": "aldi",
        "GPSlocation":
            {"lat": 42.1231, "long": 100.1},
        "Adresse": "Straße",
        "status": 1,
        "timestamp": "01-01-1970"}

    return market


@router.get('/market/<int:id>', response_model=Stammdaten)
async def get_market(id):
    """
    Endpoint: /market/
    Methods:  GET
    Parameter: MarketID - id of the market

    """
    query = sql_stammdaten.filter_by(id=id)
    return await database.fetch_one()


@router.get('/marketlist/', response_model=List[Stammdaten])
async def get_marketlist():
    query = sql_stammdaten.query(Stammdaten).all()
    return await database.fetch_all(query)


@router.put('/market/')
def set_market():
    """
    Endpoint: /market/
    Methods:  PUT
    Parameter: MarketID - id of the market
               Status   - the Status the status of the market should change to

    The function takes a json object with the key/value pairs descripted by Parameters and
    initiates the corresponding db change.
    """
    content = get_validated_json(SETMARKETSCHEMA)
    success = update_market_status(content['MarketID'], content['Status'])
    return {"Success": success}


@router.post('/market/')
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
        success = create_market_entity(content['MarketID'], content['Name'], content["Company"], content["GPSLocation"]
                                       ["Lat"], content["GPSLocation"]["Long"], content["Adresse"], content["Enabled"], content["Status"])
        return {"Success": success}
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


def create_market_entity(market_id, name, company, lat, long, adress, enabled, status):
    print(market_id, name, company, lat, long, enabled, status)
    market = Stammdaten(id=market_id, name=name, company=company, lat=lat,
                        long=long, adresse=adress, enabled=enabled, status=status)

    db.session.add(market)
    db.session.commit()
    return True
