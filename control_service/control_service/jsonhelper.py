from control_service.models import Stammdaten


def market_to_obj(market: Stammdaten):
    if market == None:
        return None

    market_obj = {
        "MarketID": market.id,
        "Name": market.name,
        "Company": market.company,
        "GPSLocation":
        {
            "lat": market.lat,
            "long": market.long,
        },
        "Adresse": market.adresse,
        "Status": market.status,
        "TimeStamp": market.timestamp.isoformat()

    }