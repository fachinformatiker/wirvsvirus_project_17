from functools import wraps
from flask import request, abort,jsonify
import jwt
from control_service import app, auth, db
from control_service.models import UserData, Stammdaten


@app.route('/markt/<int:id>')
def get_market(id):
    return jsonify(db.session.query(Stammdaten).filter_by(id=id).first())
"""
@app.route('/markt/get')
def get_market_body():
    if(request.method == 'GET'):
        market=db.session.query(Stammdaten).filter_by(id=id).first()
        return jsonify(market)
    abort(400)
"""
@app.route('/marktlist/')
def get_marketlist():
    if (request.method == 'GET'):
        return jsonify(db.session.query(Stammdaten).all())
    abort(400)


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
    if (request.is_json == True and request.method == 'POST'):
        content = request.get_json()
        if (auth.validate_auth_token(content['MarketID'], content['Token'])):
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


# @authorize_token
# def update_market_status(current_user):
def update_market_status(market_id, status):
    # market = Stammdaten.query.filter_by(id=market_id).first()
    market = db.session.query(Stammdaten).filter_by(id=market_id).first()
    if (market.status != status):
        market.status = status
        db.session.commit()
        return True
    else:
        return False


def authorize_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return {
                "Error": 'token not valid'
            }
