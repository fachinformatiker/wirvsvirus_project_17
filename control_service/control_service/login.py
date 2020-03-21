from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app


@app.route('/Login', methods=['POST'])
def login():
    try:
        data = request.json

        username = data['Username']
        password = data['Password']

        # @TODO: DB Client

        response = {}
        response['Token'] = "FancyBearerToken"

        return jsonify(response)
    except Exception:
        abort(400)