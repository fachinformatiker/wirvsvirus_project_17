from input_service import db
from input_service.models import Stammdaten, UserData

def validate_auth_token(id, token):
  validator_token = get_market_token(id)
  if(token == validator_token):
    return True
  else:
    return False

def get_market_token(market_id):
  markt = Stammdaten.query.filter_by(id=market_id).first()
  return markt.super_user.token