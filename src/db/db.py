from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models.models import User

app = create_app()

def create_db():
    app.config.from_object('config.config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    db = SQLAlchemy(app)
    db.create_all()
    return db

# class CreateSchem:
#     , Desk, Task




