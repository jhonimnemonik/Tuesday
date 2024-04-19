from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from models.models import User
from views import db, menu

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def home():
    if not "userLogged" in session:
        return render_template("home/index.html", menu=menu, page="home", user=None)
    if "userLogged" in session:
        return redirect(url_for("user_routes.profile", username=session["userLogged"]))


@home_routes.route("/login", methods=["GET", "POST"])
def login():
    if "userLogged" in session:
        return redirect(url_for("user_routes.profile", username=session["userLogged"])), 301

    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["userLogged"] = username
            flash(f"Авторизация прошла успешно. Приветствуем {username}!", "success")
            return redirect(url_for("user_routes.profile", username=username))
        else:
            flash("Неправильное имя пользователя или пароль", "error")

    return redirect(url_for("user_routes.profile"))


@home_routes.route("/logout")
def logout():
    session.pop("userLogged", None)
    flash("Вы успешно вышли из аккаунта", "success")
    return redirect(url_for("home_routes.home", menu=menu, page="home"))


@home_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password2"]
        is_valid, error_message = User.validate_registration(username, password, password2, email)
        if not is_valid:
            flash(error_message, "error")
            return render_template("user/register.html", menu=menu)
        # existing_user = User.query.filter_by(username=username).first()
        # if existing_user:
        if User.query.filter_by(username=username).first():
            flash("Пользователь с таким именем уже существует!", "error")
            return redirect(url_for("home_routes.register", menu=menu))
        else:
            new_user = User(username=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash(error_message, "success")
            return redirect(url_for("home_routes.login", menu=menu, page="home"))

    return render_template("home/register.html", menu=menu, user=None)
