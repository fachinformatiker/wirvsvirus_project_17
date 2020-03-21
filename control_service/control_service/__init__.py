from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET'] = 'RemoveMeFromProduction'

db = SQLAlchemy(app)


import control_service.models
import control_service.views
import control_service.viewsdynamic
import control_service.register
import control_service.login
import control_service.getUserProfil

db.create_all()