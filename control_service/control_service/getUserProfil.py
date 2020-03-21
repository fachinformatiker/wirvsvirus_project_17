from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app


@app.route('/GetUserProfil', methods=['POST'])
def getUserProfil():
    try:
        data = request.json

        reqToken = data['Token']

        userEntity = db.session.query(UserData).filter_by(token == reqToken).first()

        response = {}
        response['Username'] = userEntity['user_name']
        response['MarketId'] = userEntity['market_id']

        return jsonify(response)
    except Exception:
        abort(400)