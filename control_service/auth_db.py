
#todo: rewrite whole thing

# http://flask.pocoo.org/docs/1.0/tutorial/database/

import click
import os
from flask import Flask, redirect, request, url_for

from flask import current_app, g
from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy


def get_db():
	if "db" not in g:
		g.db = SQLAlchemy()
	return g.db

def close_db(e=None):
	db = g.pop("db", None)

	if db is not None:
		db.close()

def init_db():
	db = get_db()


@click.command("init-db")
@with_appcontext
def init_db_command():
	"""Clear the existing data and create new tables."""
	init_db()
	click.echo("Initialized the database.")

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
