from flask_login import UserMixin
from flask import g

from flask_sqlalchemy import SQLAlchemy
from auth_db import get_db

#def init_user_func():
db = SQLAlchemy()
#	return

#todo replace pic with adress or equivalent
class User(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(40))
	email = db.Column(db.String(40))
	profile_pic = db.Column(db.String(40))
		
	@staticmethod
	def get(user_id):
		ldb = get_db()
		user = ldb.session.query(User).filter_by(id==user_id).first()		
		if user == None:
				return None
		user = User(
			id=user[0], name=user[1], email=user[2], profile_pic=user[3]
		)
		return user

	@staticmethod
	def create(id, name, email, profile_pic):
		ldb = get_db()
		user = User(id, name, email, profile_pic)
		ldb.session.add(user)
		ldb.session.commit()
		