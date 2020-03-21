from flask import request, abort
from input_service import app, auth

@app.route('/market/status', methods=['POST'])
def set_market_status():
  if(request.is_json == True):
    content = request.get_json()
    if(auth.validate_auth_token(content['id'], content['token'])):
      payload = query_market_status(content['id'])
      return payload
    #if request.method == 'POST':
    else:
      abort(400)
  else:
    abort(400)

def query_market_status(id):
  return 'VALIDATED'