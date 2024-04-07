from db.db import create_db

db = create_db()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)


# class Desk(db.Model):
#     pass
#
#
# class Task(db.Model):
#     pass
