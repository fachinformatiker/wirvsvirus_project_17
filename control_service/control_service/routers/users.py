from fastapi import APIRouter, HTTPException
#from flask import Blueprint, jsonify, request, abort
from functools import wraps
from control_service.models import UserData, sql_userdata,database
#from control_service.schemas import REGISTERSCHEMA, get_validated_json, PROFILESCHEMA,LOGINSCHEMA
#from werkzeug.security import generate_password_hash
from secrets import token_urlsafe
router = APIRouter()

@router.post('/Register')
def register():
    data = get_validated_json(REGISTERSCHEMA)

    username = data['Username']
    password = data["Password"]

    userEntity = db.session.query(UserData).filter_by(
        user_name=username).first()

    response = {}
    if userEntity != None:
        response['Success'] = False
        return response
    else:
        user = UserData(user_name=username, password=generate_password_hash(password), token=token_urlsafe())
        db.session.add(user)
        db.session.commit()

        response['Success'] = True
        return response

@router.post('/Login')
def login():
    data = get_validated_json(LOGINSCHEMA)

    reqUsername = data['Username']
    reqPassword = data['Password']

    userEntity = UserData.filter_by(user_name = reqUsername).first()

    response = {}
    if userEntity is not None:
        response['Token'] = userEntity.token
    else:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not check_password_hash(userEntity.password, reqPassword):
        raise HTTPException(status_code=403, detail="Forbidden")

    return response
