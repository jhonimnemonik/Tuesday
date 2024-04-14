import os
import base64
from __main__ import app, db
from flask_login import UserMixin
from hashlib import sha3_256
import re


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     boards = db.relationship('Board', backref='user', lazy=True)
#
#     def __init__(self, username, password):
#         self.username = username
#         self.password_hash = self._hash_password(password)
#
#     def _hash_password(self, password):
#         custom_salt = app.config['SECRET_KEY']
#         salt = os.urandom(32)
#         h_pswrd = sha3_256(password.encode("utf-8")).digest()
#         mix = bytes([s ^ p for s, p in zip(salt, h_pswrd)])
#         h_pswrd = sha3_256(mix).digest()
#         scrt_key = sha3_256(custom_salt.encode("utf-8")).digest()
#         mix = bytes([s ^ p for s, p in zip(scrt_key, h_pswrd)])
#         h_pswrd = sha3_256(mix).digest()
#         hashed_password = f"{base64.b64encode(h_pswrd).decode('utf-8')}.\
#             {base64.b64encode(salt).decode('utf-8')}"
#         return hashed_password
#
#     def check_password(self, password_to_check):
#         stored_password, salt = self.password_hash.split('.')
#         salt = base64.b64decode(salt)
#         hashed_password = self._hash_password_with_salt(password_to_check, salt)
#         return hashed_password == stored_password
#
#     def _hash_password_with_salt(self, password, salt):
#         custom_salt = app.config['SECRET_KEY']
#         h_pswrd = sha3_256(password.encode("utf-8")).digest()
#         mix = bytes([s ^ p for s, p in zip(salt, h_pswrd)])
#         h_pswrd = sha3_256(mix).digest()
#         scrt_key = sha3_256(custom_salt.encode("utf-8")).digest()
#         mix = bytes([s ^ p for s, p in zip(scrt_key, h_pswrd)])
#         h_pswrd = sha3_256(mix).digest()
#         hashed_password = f"{base64.b64encode(h_pswrd).decode('utf-8')}"
#         return hashed_password


def validate_password(password):
    r_p = re.compile(r'^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
    return r_p.match(password)


def validate_name(name):
    r_p = re.compile(r'^[a-zA-Z0-9_-]{3,16}$')
    return r_p.match(name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    boards = db.relationship('Board', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password):
        custom_salt = app.config['SECRET_KEY']
        salt = os.urandom(32)
        h_pswrd = sha3_256(password.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(salt, h_pswrd)])
        h_pswrd = sha3_256(mix).digest()
        scrt_key = sha3_256(custom_salt.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(scrt_key, h_pswrd)])
        h_pswrd = sha3_256(mix).digest()
        hashed_password = f"{base64.b64encode(h_pswrd).decode('utf-8')}.\
            {base64.b64encode(salt).decode('utf-8')}"
        return hashed_password

    def check_password(self, password_to_check):
        stored_password, salt = self.password_hash.split('.')
        salt = base64.b64decode(salt)
        hashed_password = self._hash_password_with_salt(password_to_check, salt)
        return hashed_password == stored_password

    def _hash_password_with_salt(self, password, salt):
        custom_salt = app.config['SECRET_KEY']
        h_pswrd = sha3_256(password.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(salt, h_pswrd)])
        h_pswrd = sha3_256(mix).digest()
        scrt_key = sha3_256(custom_salt.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(scrt_key, h_pswrd)])
        h_pswrd = sha3_256(mix).digest()
        hashed_password = f"{base64.b64encode(h_pswrd).decode('utf-8')}"
        return hashed_password



class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ContactMessage {self.id}>'


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='board', lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)


class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)