from flask import request, abort
from input_service import app, auth, db
from input_service.models import UserData, Stammdaten

@app.route('/market/status', methods=['POST'])
def set_market_status():
  if(request.is_json == True):
    content = request.get_json()
    if(auth.validate_auth_token(content['id'], content['token'])):
      payload = update_market_status(content['id'], content['status'])
      return payload
    #if request.method == 'POST':
    else:
      abort(400)
  else:
    abort(400)

def update_market_status(market_id, status):
  market = Stammdaten.query.filter_by(id=market_id).first()
  if(market.status != status):
    market.status = status
    print(market.timestamp)
    db.session.commit()
    print(market.timestamp)
    return 'STATUS UPDATED'
  else:
    abort(400)