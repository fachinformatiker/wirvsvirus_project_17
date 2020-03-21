from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app


@app.route('/GetUserProfil', methods=['POST'])
def getUserProfil():
    try:
        data = request.json

        username = data['Token']

        # @TODO: DB Client

        response = {}
        response['Username'] = "ChuckNorris"
        response['MarketId'] = 4711

        return jsonify(response)
    except Exception:
        abort(400)