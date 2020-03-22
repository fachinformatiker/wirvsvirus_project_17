from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['CONNECTION_STRING']
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