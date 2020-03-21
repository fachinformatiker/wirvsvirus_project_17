from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app, db
from control_service.models import UserData
from control_service.schemas import LOGINSCHEMA, get_validated_json


@app.route('/Login', methods=['POST'])
def login():
    data = get_validated_json(LOGINSCHEMA)

    reqUsername = data['Username']
    reqPassword = data['Password']

    userEntity = db.session.query(UserData).filter_by(user_name = reqUsername, password = reqPassword).first()

    response = {}
    if(userEntity != None):
        response['Token'] = userEntity['token']

    return jsonify(response)