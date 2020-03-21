from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app, db
from control_service.models import UserData


@app.route('/Login', methods=['POST'])
def login():
    try:
        data = request.json

        reqUsername = data['Username']
        reqPassword = data['Password']

        userEntity = db.session.query(UserData).filter_by(user_name == reqUsername, password == reqPassword).first()

        response = {}
        response['Token'] = userEntity['token']

        return jsonify(response)
    except Exception:
        abort(400)