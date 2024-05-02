from flask import render_template, flash, abort, session
from __main__ import app, db
from functools import wraps

from models.models import User

app = app
db = db
menu = [
    {"name": "Главная", "url": "/", "page": "home"},
    {"name": "О нас", "url": "/about", "page": "about"},
    {"name": "Контакт", "url": "/contact", "page": "contact"},
    {"name": "Мои проекты", "url": "/profile/projects/", "page": "board"},
    {"name": "Профиль", "url": "/profile", "page": "profile"},
]


@app.errorhandler(500)
def handle_500(error):
    return render_template("error/page500.html", menu=menu), 500


@app.errorhandler(401)
def handle_401(error):
    return render_template("error/page401.html", menu=menu, username=session.get("userLogged")), 401


@app.errorhandler(403)
def handle_403(error):
    return render_template("error/page401.html", menu=menu, username=session.get("userLogged")), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error/page404.html", menu=menu, username=session.get("userLogged")), 404


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in kwargs:
            username = kwargs["username"]
        else:
            username = None

        if "userLogged" not in session or session["userLogged"] != username:
            flash("Вы не авторизованы.", "error")
            abort(401)
        return f(*args, **kwargs)

    return decorated_function


def chk_user():
    if "userLogged" in session:
        username = session["userLogged"]
        user = User.query.filter_by(username=username).first()
        user_id = user.id
        return user_id, username, user
    else:
        return None, None, None
