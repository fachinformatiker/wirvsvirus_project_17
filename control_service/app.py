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
from auth_db import init_db_command
#from user import User, init_user_func


from flask_login import UserMixin

# Flask app setup

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

#custom config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
	"https://accounts.google.com/.well-known/openid-configuration"
)

#init_user_func()

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
	return "You must be logged in to access this content.", 403


# Naive database setup
try:
	init_db_command()
except:
		pass
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
	user = User(id=unique_id, name=users_name, email=users_email, profile_pic=picture)
	#user = temp_user.create(id_=unique_id, name=users_name, email=users_email, profile_pic=picture)

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
	
	