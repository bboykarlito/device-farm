from flask import current_app, g
from flask_pymongo import PyMongo


def get_db():
    if "db" not in g:
        g.db = PyMongo(current_app).db

    return g.db


def close_db(e=None):
    g.pop("db", None)


def init_app(app):
    app.teardown_appcontext(close_db)
