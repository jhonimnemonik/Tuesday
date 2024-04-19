from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlite3
from flask import current_app, g


def create_db(app):
    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db, command="db")
    return db, migrate


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
