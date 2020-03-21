from input_service import db
from input_service.models import Stammdaten, UserData

"""
Paramter: market_id - ID des Marktes
          token - der in der Anfrage übergebenen Token

Die Funktion ruft den, in der Datenbank hinterlegten, zugehörigen Token für die angegebene Markt ID
und vergleicht diesen mit dem in der Anfrage übermittelten Token
"""
def validate_auth_token(market_id, token):
  validator_token = get_market_token(market_id)
  if(token == validator_token):
    return True
  else:
    return False

"""
Parameter: market_id - ID des Marktes

Die Funktion ruft den Token des zum Markt gehörenden Users aus der Datenbank ab.
"""
def get_market_token(market_id):
  markt = db.session.query(Stammdaten).filter_by(id=market_id).first()
  #markt = db.session.query(UserData.token).filter_by(id=market_id).first()
  return markt.super_user.token