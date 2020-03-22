from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app, db
from control_service.models import UserData
from control_service.schemas import REGISTERSCHEMA, get_validated_json
from werkzeug.security import generate_password_hash
from secrets import token_urlsafe


@app.route('/Register', methods=['POST'])
def register():
    data = get_validated_json(REGISTERSCHEMA)

    username = data['Username']
    password = data["Password"]

    userEntity = db.session.query(UserData).filter_by(
        user_name=username).first()

    response = {}
    if userEntity != None:
        response['Success'] = False
        return jsonify(response)
    else:
        user = UserData(user_name=username, password=generate_password_hash(password), token=token_urlsafe())
        db.session.add(user)
        db.session.commit()

        response['Success'] = True
        return jsonify(response)
