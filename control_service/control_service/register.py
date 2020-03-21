from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app, db
from control_service.models import UserData
from control_service.schemas import REGISTERSCHEMA, get_validated_json


@app.route('/Register', methods=['POST'])
def register():
    data = get_validated_json(REGISTERSCHEMA)

    username = data['Username']

    userEntity = db.session.query(UserData).filter_by(
        user_name=username).first()

    response = {}
    if userEntity != None:
        response['Success'] = False
        return jsonify(response)
    else:
        # @TODO: OAuth

        response['Success'] = True
        return jsonify(response)
