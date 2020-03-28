from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app, db
from control_service.models import UserData
from control_service.schemas import PROFILESCHEMA, get_validated_json


@app.route('/GetUserProfil', methods=['POST'])
def getUserProfil():
    data = get_validated_json(PROFILESCHEMA)

    reqToken = data['Token']

    userEntity = db.session.query(UserData).filter_by(token = reqToken).first()

    response = {}
    response['Username'] = userEntity['user_name']
    response['MarketId'] = userEntity['market_id']

    return jsonify(response)