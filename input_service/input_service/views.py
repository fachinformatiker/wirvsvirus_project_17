from flask import request, abort
from input_service import app, auth, db
from input_service.models import UserData, Stammdaten


"""
Endpoint: /market/status
Methods: POST
Parameter: MarketID - ID des Marktes
           Token - Bearer Token des Users welcher als super_user des Marktes eingetragen ist
           Status - der Status
          
Die Funktion nimmt die POST Anfrage entgegen, 
überprüft ob die Daten als json vorliegen und ruft dann Authentizierung und Datenupdate auf.
"""
@app.route('/market/status', methods=['POST'])
def set_market():
  if(request.is_json == True and request.method == 'POST'):
    content = request.get_json()
    if(auth.validate_auth_token(content['MarketID'], content['Token'])):
      success = update_market_status(content['MarketID'], content['Status'])
      return {
        "Success": success
      }
    else:
      abort(400)
  else:
    abort(400)

"""
Paramter: market_id - ID des Marktes
          status - der neue Status

Die Funktion überprüft, ob sich der neue Status von dem alten unterscheidet und führt dann das Datenbankupdate durch.
"""
def update_market_status(market_id, status):
  market = Stammdaten.query.filter_by(id=market_id).first()
  if(market.status != status):
    market.status = status
    db.session.commit()
    return True
  else:
    return False