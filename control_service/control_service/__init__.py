from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET'] = 'RemoveMeFromProduction'
cache = Cache(app,config={'CACHE_TYPE': 'null'}) #disabled

db = SQLAlchemy(app)


import control_service.models
import control_service.views
import control_service.viewsdynamic
db.create_all()