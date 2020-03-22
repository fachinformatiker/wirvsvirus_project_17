from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os

app = Flask(__name__)
conn_string=os.environ.get("CONNECTION_STRING")

if conn_string is None:
    conn_string="sqlite:////tmp/test.db"
app.config['SQLALCHEMY_DATABASE_URI'] =conn_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cache = Cache(app,config={'CACHE_TYPE': "simple"}) #disabled

db = SQLAlchemy(app)


import control_service.models
import control_service.views
import control_service.viewsdynamic
import control_service.register
import control_service.login
import control_service.getUserProfil

db.create_all()