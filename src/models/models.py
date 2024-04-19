import os
import base64
import re
from datetime import datetime
from flask_login import UserMixin
from hashlib import sha3_256
from __main__ import app, db

'''For migrate only! '''
# from app import app, db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    date_reg = db.Column(db.Date, default=datetime.utcnow)
    boards = db.relationship("Board", backref="user", lazy=True, foreign_keys="[Board.user_id]")

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)

    @staticmethod
    def validate_registration(username, password, password2, email):
        if not re.match(r"^[a-zA-Z0-9_-]{3,16}$", username):
            return (
                False,
                "Имя должно содержать от 3-16 символов, состоять только из заглавных и прописных букв латинского алфавита, может также содержать цифры, и символы '_', '-'!",
            )
        if password != password2:
            return False, "Пароли не совпадают!"
        if not (re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email)):
            return False, "Проверьте правильность email!"
        if not re.match(r"^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])", password):
            return (
                False,
                """Пароль должен быть от 8-20 символов, содержать латинские хотя бы одну
            заглавную и маленькую буквы, и хотя бы одну цифру, хотя бы один спец символ!""",
            )
        return True, "Регистрация успешно завершена!"

    def _hash_password(self, password):
        custom_salt = app.config["SECRET_KEY"]
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
        stored_password, salt = self.password_hash.split(".")
        salt = base64.b64decode(salt)
        hashed_password = self._hash_password_with_salt(password_to_check, salt)
        return hashed_password == stored_password

    def _hash_password_with_salt(self, password, salt):
        custom_salt = app.config["SECRET_KEY"]
        h_pswrd = sha3_256(password.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(salt, h_pswrd)])
        h_pswrd = sha3_256(mix).digest()
        scrt_key = sha3_256(custom_salt.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(scrt_key, h_pswrd)])
        h_pswrd = sha3_256(mix).digest()
        hashed_password = f"{base64.b64encode(h_pswrd).decode('utf-8')}"
        return hashed_password


class TeamUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User", backref="teams_owned", foreign_keys="[TeamUser.owner_id]")
    username = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    boards = db.relationship("Board", backref="team_user", lazy=True, foreign_keys="[Board.team_user_id]")

    def __init__(self, username, owner, boards):
        self.username = username
        self.owner = owner
        self.boards = boards


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ContactMessage {self.id}>"

    @staticmethod
    def validate_data(email, name):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if not (re.fullmatch(regex, email)):
            return False, "Проверьте email."
        r_n = re.compile(r"^[a-zA-Z0-9_-]{3,16}$")
        if not r_n.match(name):
            return (
                False,
                """Имя должно содержать от 3-16 символов, состоять только из заглавных 
            и прописных букв латинского алфавита, может также содержать цирфры, и символы "_", "-"!.""",
            )
        return True, "Сообщение отправлено."


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    team_user_id = db.Column(db.Integer, db.ForeignKey("team_user.id"), nullable=True)
    tasks = db.relationship("Task", backref="board", lazy=True)

    def __init__(self, user_id, name=None, team_user_id=None):
        if name is None:
            last_board = Board.query.order_by(Board.id.desc()).first()
            if last_board:
                board_number = last_board.id + 1
            else:
                board_number = 1
            name = f"Доска {board_number}"
        self.name = name
        self.user_id = user_id
        self.team_user_id = team_user_id


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.SmallInteger, nullable=True)
    description = db.Column(db.Text, nullable=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    columns = db.relationship("Column", backref="task", lazy=True)
    messages = db.relationship("ChatMessage", backref="task", lazy="dynamic")

    def __init__(self, name=None, status=None, priority=None, description=None, board_id=None):
        if name is None:
            board = Board.query.get(board_id)
            if board:
                last_task = Task.query.filter_by(board_id=board_id).order_by(Task.id.desc()).first()
                if last_task:
                    task_number = last_task.id + 1
                else:
                    task_number = 1
                name = f"Задача {task_number}"
            else:
                raise ValueError("Invalid board_id provided")
        self.name = name
        self.status = status
        self.priority = priority
        self.description = description
        self.board_id = board_id


class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # tasks = db.relationship("Task", secondary="column_content", backref="columns")
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    # task = db.relationship("Task", backref=db.backref("columns", cascade="all, delete-orphan"))


class ColumnContent(db.Model):
    column_id = db.Column(db.Integer, db.ForeignKey("column.id"), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    column = db.relationship("Column", backref="contents")
    task = db.relationship("Task", backref="contents")

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "sender_id": self.sender_id,
            "text": self.text,
            "timestamp": self.timestamp.isoformat(),
        }
