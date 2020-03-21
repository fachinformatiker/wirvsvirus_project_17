from flask import Blueprint, jsonify, request
from flask.json import jsonify

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
        response = {}
        response['Success'] = False
        return jsonify(response)