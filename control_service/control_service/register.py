from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app, db
from control_service.models import UserData


@app.route('/Register', methods=['POST'])
def register():
    try:
        data = request.json

        username = data['Username']
        password = data['Password']

        userEntity = db.session.query(UserData).filter_by(user_name == username, password == password).first()

        response = {}
        if(userEntity != null):
            response['Success'] = False
            return jsonify(response)
        else:
            # @TODO: OAuth

            response['Success'] = True
            return jsonify(response)
        
        
    except Exception:
        abort(400)