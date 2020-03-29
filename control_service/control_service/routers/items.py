from fastapi import APIRouter,Depends
from typing import List
from control_service.models import  Stammdaten, sql_stammdaten,database, Market_status,UserData
from control_service.routers.users import get_current_active_user

router = APIRouter()


@router.get('/')
async def hello_world():
    return 'Hello World!'


@router.get('/static/markt/')
async def get_marketstatic():
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
    query = sql_stammdaten.select().where(sql_stammdaten.c.MarketID==id)
    return await database.fetch_one(query)


@router.get('/marketlist/', response_model=List[Stammdaten])
async def get_marketlist(x, y, width, heigth):
    """
    Endpoint: /marketlist/
    Methods:  GET
    Parameter:  x       - x coordinate bottom left
                y       - x coordinate bottom left
                width   - screen width
                heigth  - screen heigth

    """
    query = sql_stammdaten.select().where(sql_stammdaten.c.lat >= x).where(sql_stammdaten.c.lat < x+width).where(sql_stammdaten.c.long >= y).where(sql_stammdaten.c.long < y+heigth).select()
    return await database.fetch_all(query)


@router.put('/market/')
async def set_market(status: Market_status):
    """
    Endpoint: /market/
    Methods:  PUT
    Parameter: MarketID - id of the market
               Status   - the Status the status of the market should change to

    The function takes a json object with the key/value pairs descripted by Parameters and
    initiates the corresponding db change.
    """
    query = sql_stammdaten.update().where(sql_stammdaten.c.MarketID == status.MarketID).values(Status=status.Status)
    result= await database.execute(query)
    return {"Success": result}


@router.post('/market/')
async def create_market(item: Stammdaten,current_user: UserData = Depends(get_current_active_user)):
    """
    Endpoint: /market/
    Methods:  POST
    Parameter:
    id=market_id, name=name, company=company, lat=lat,
                        long=long, adresse=adress, enabled=enabled, status=status
    """
    query = sql_stammdaten.insert().values(
        MarketID=item.MarketID,
        Name=item.Name,
        Firma=item.Firma,
        lat=item.lat,
        long=item.long,
        Adresse=item.Adresse,
        Enabled=item.Enabled,
        Status=item.Status
        )
    last_record_id= await database.execute(query)
    return last_record_id
