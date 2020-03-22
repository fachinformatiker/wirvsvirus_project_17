from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

app = Flask(__name__)
#app.config.from_envvar('CONTROL_SERVICE_SETTINGS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cache = Cache(app,config={'CACHE_TYPE': 'null'}) #disabled

db = SQLAlchemy(app)


import control_service.models
import control_service.views
import control_service.viewsdynamic
import control_service.register
import control_service.login
import control_service.getUserProfil

db.create_all()