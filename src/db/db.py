import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_db(app):
    app.config.from_object('config.config.Config')
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    db = SQLAlchemy(app)

    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db, command='migrate')
    return db, migrate





