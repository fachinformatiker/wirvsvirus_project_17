import requests
from flask import request, abort
from input_service import app

@app.route('/market/status', methods=['POST'])
def handle_market_status_change():
  content = request.json
  market_id = content['MarketID']
  token = content['Token']
  status = content['Status']

  try:
    auth_request = requests.post('http://controlservice/GetUserProfil', data = {'Token':token}, verify=False)
  except requests.exceptions.ConnectionError:
    abort(400)

  auth_response = auth_request.json()

  if auth_response['MarketId'] == market_id:
    try:
      status_update_request = requests.post('http://controlservice/market/status', data = {'MarketId': market_id, 'Status': status}, verify=False)
    except requests.exceptions.ConnectionError:
      abort(400)
  
  status_update_response = status_update_request.json()

  return {
    "Success": status_update_response['Success']
  }