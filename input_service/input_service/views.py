from flask import request
from input_service import app, auth

@app.route('/market/status', methods=['POST'])
def set_market_status():
  if(request.is_json()):
    content = request.get_json()
    if(auth.validate_auth_token(content['token'])):
      query_market_status(content['id'])
    if request.method == 'POST':
      return 'Hello'

def query_market_status(id):
  return 0