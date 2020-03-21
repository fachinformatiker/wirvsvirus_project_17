from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service import app

register = Blueprint('register', __name__)

@register.route('/register/v1', methods=['POST'])
def index():
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