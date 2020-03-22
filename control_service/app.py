import json
import os
import click

# Third party libraries
from flask import Flask, redirect, request, url_for, g
from flask_login import (
	LoginManager,
	current_user,
	login_required,
	login_user,
	logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext


# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

#custom config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Internal imports
#from user import User


#custom imports
#from bearer_token import Token


# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
	"https://accounts.google.com/.well-known/openid-configuration"
)


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
	return "You must be logged in to access this content.", 403


# Naive database setup
#try:
init_db_command()
	#except 
	#	pass
#catch error with db creation

# OAuth2 client setup
newClient = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)



@app.route("/")
def index():
	if current_user.is_authenticated:
		# bearer token
		return (
			"<p>Hello, {}! You're logged in! Email: {}</p>"
			"<div><p>Google Profile Picture:</p>"
			'<img src="{}" alt="Google profile pic"></img></div>'
			'<a class="button" href="/logout">Logout</a>'.format(
				current_user.name, current_user.email, current_user.profile_pic
			)
		)
	else:
		return '<a class="button" href="/login">Google Login</a>'


#todo: receive Login() request
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
	request_uri = newClient.prepare_request_uri(
		authorization_endpoint,
		redirect_uri=request.base_url + "/callback",
		scope=["openid", "email", "profile"],
	)
	return redirect(request_uri)
#todo: change this? or use different function to redirect: redirect_uri=request.base_url + "/callback"


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
	code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
	token_url, headers, body = newClient.prepare_token_request(
		token_endpoint,
		authorization_response=request.url,
		redirect_url=request.base_url,
		code=code,
	)
	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
	)

    # Parse the tokens!
	newClient.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	uri, headers, body = newClient.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
	if userinfo_response.json().get("email_verified"):
		unique_id = userinfo_response.json()["sub"]
		users_email = userinfo_response.json()["email"]
		picture = userinfo_response.json()["picture"]
		users_name = userinfo_response.json()["given_name"]
	else:
		return "User email not available or not verified by Google.", 400

	#todo: change to new model
    # Create a user in our db with the information provided by Google
	user = User(
		id_=unique_id, name=users_name, email=users_email, profile_pic=picture
	)

    # Doesn't exist? Add to database
	if not User.get(unique_id):
		User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
	login_user(user)
	
    # Send user back to homepage
	return redirect(url_for("index"))

	#try again later
	'''
	token = Token(id, client_id, client, user_id, user, token_type)
	#request kann so verwendet werden?
	bearer = savetoken(token, request, *args, **kwargs)
	#send token?
    return bearer #redirect?
	'''

@app.route("/logout")
@login_required
def logout():
	logout_user()

	return redirect(url_for("index"))


def get_google_provider_cfg():
	return requests.get(GOOGLE_DISCOVERY_URL).json()


if __name__ == "__main__":
	app.run(ssl_context="adhoc")
	
	
#todo replace pic with adress or equivalent
class User(UserMixin):
	def __init__(self, id_, name, email, profile_pic):
		self.id = id_
		self.name = name
		self.email = email
		self.profile_pic = profile_pic

	@staticmethod
	def get(user_id):
		user = db.query(User).filter_by(id==user_id).first()		
		if user == None:
				return None
		user = User(
			id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
		)
		return user

	@staticmethod
	def create(id_, name, email, profile_pic):
		user = User(id, name, email, profile_pic)
		db.session.add(user)
		db.session.commit()
		
class Client(db.Model):
    # human readable name, not required
	name = db.Column(db.String(40))

    # creator of the client, not required
	user_id = db.Column(db.ForeignKey('user.id'))
    # required if you need to support client credential
	user = db.relationship('User')

	client_id = db.Column(db.String(40), primary_key=True)
	client_secret = db.Column(db.String(55), unique=True, index=True,
			nullable=False)

	email = sb.Column(db.String(40), unique=True)
	
	#change to adress/coordinates
	profile_pic = db.Column(db.String(40), nullable=False)

    # public or confidential
	is_confidential = db.Column(db.Boolean)

	_redirect_uris = db.Column(db.Text)
	_default_scopes = db.Column(db.Text)

	@property
	def client_type(self):
		if self.is_confidential:
			return 'confidential'
		return 'public'

	@property
	def redirect_uris(self):
		if self._redirect_uris:
			return self._redirect_uris.split()
		return []

	@property
	def default_redirect_uri(self):
		return self.redirect_uris[0]

	@property
	def default_scopes(self):
		if self._default_scopes:
			return self._default_scopes.split()
		return []
	
	
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
									 
									 
@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()

from datetime import datetime, timedelta

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(client_id=request.client.client_id,
                                 user_id=request.user.id)
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok