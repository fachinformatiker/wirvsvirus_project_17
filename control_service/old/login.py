from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app, db
from control_service.models import UserData
from control_service.schemas import LOGINSCHEMA, get_validated_json
from werkzeug.security import check_password_hash


@app.route('/Login', methods=['POST'])
def login():
    data = get_validated_json(LOGINSCHEMA)

    reqUsername = data['Username']
    reqPassword = data['Password']

    userEntity = db.session.query(UserData).filter_by(user_name = reqUsername).first()

    response = {}
    if userEntity is not None:
        response['Token'] = userEntity.token
    else:
        abort(403)

    if not check_password_hash(userEntity.password, reqPassword):
        abort(403)

    return jsonify(response)