from control_service import db

"""
Die Models entsprechend der API Beschreibung mit einer One-to-One Relation
"""
class Stammdaten(db.Model):
  id = db.Column(db.Integer,name='MarketID', primary_key=True)
  name = db.Column(db.String(100), name='Name', unique=False, nullable=False)
  company = db.Column(db.String(100),name='Firma', unique=False, nullable=False)
  lat=db.Column(db.String(10),name='lat', unique=False, nullable=False)
  long=db.Column(db.String(10), name='long', unique=False, nullable=False)
  adresse = db.Column(db.String(50),name='Adresse', unique=False, nullable=False)
  enabled = db.Column(db.Boolean, name='Enabled')
  super_user = db.relationship('UserData', uselist=False, backref='market')
  status = db.Column(db.Integer, name='Status')
  timestamp = db.Column(db.DateTime, name='TimeStamp', server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())

class UserData(db.Model):
  id = db.Column(db.Integer,name='UserID', primary_key=True)
  user_name = db.Column(db.String(20),name='UserName', unique=False, nullable=False)
  password = db.Column(db.String(100))
  rolle = db.Column(db.Integer, name='Rolle')
  mail = db.Column(db.String(50), name='Email')
  telefon = db.Column(db.String(20), name='Telefon')
  market_id = db.Column(db.Integer, db.ForeignKey('stammdaten.MarketID'))
  token = db.Column(db.String(64), name='BearerToken', unique=True)