from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app


@app.route('/Register', methods=['POST'])
def register():
    try:
        data = request.json

        username = data['Username']
        password = data['Password']

        # @TODO: DB Client

        response = {}
        response['Success'] = True

        return jsonify(response)
    except Exception:
        abort(400)