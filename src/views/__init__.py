from flask import render_template, request, flash, abort, session
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
def handle_500(err):
    return render_template("error/page500.html", menu=menu), 500


@app.errorhandler(401)
def handle_401(err):
    return render_template("error/page401.html", menu=menu), 401


@app.errorhandler(404)
def page_not_found(error):
    # return render_template("error/page404.html", menu=menu, user=None), 404
    return render_template("error/page404.html", menu=menu, username=session.get("userLogged")), 404

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "userLogged" not in session:
            flash("Вы не авторизованы.", "error")
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function

def check_request_method(*methods):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method not in methods:
                flash("Недопустимый метод запроса.", "error")
                return abort(405)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def chk_user():
    username = session["userLogged"]
    user = User.query.filter_by(username=username).first()
    user_id = user.id
    return user_id, username