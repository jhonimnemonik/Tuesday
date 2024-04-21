from flask import render_template, request, redirect, url_for, flash, session, abort, Blueprint
from forms.forms import EditProfileForm
from models.models import User, Board
from views import db, menu

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/profile", methods=["GET"])
def profile():
    if "userLogged" not in session:
        flash("Вы не авторизованы.", "error")
        return redirect(url_for("home_routes.home"))
    username = session["userLogged"]
    return redirect(url_for("user_routes.profile_with_username", username=username))


@user_routes.route("/profile/<username>")
def profile_with_username(username):
    if "userLogged" not in session or session["userLogged"] != username:
        return abort(401)
    else:
        user = User.query.filter_by(username=username).first()
        boards = Board.query.filter_by(user_id=user.id).all()
        if boards:
            for board in boards:
                board_id = board.id
            return render_template("user/profile.html", menu=menu, page="profile", user=user, username=username, board=board_id)
        else:
            return render_template("user/profile.html", menu=menu, page="profile", user=user, username=username)


@user_routes.route("/profile/info", methods=["GET"])
def profile_info():
    if "userLogged" not in session:
        flash("Вы не авторизованы.", "error")
        return redirect(url_for("home_routes.home"))
    user, username = session["userLogged"]
    if user.boards:
        boards = Board.query.all()
        if boards:
            for board in boards:
                board_id = board.id
    return redirect(url_for("user_routes.profile_info_get", username=username, board_id=board_id))


@user_routes.route("/profile/<username>/info", methods=["GET"])
def profile_info_get(username):
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)
    user = User.query.filter_by(username=username).first()
    return render_template("user/user_info.html", menu=menu, page="profile", user=user)


@user_routes.route("/edit-profile", methods=["GET"])
def edit_profile():
    if "userLogged" not in session:
        flash("Вы не авторизованы.", "error")
        return redirect(url_for("home_routes.home"))
    username = session["userLogged"]
    return redirect(url_for("user_routes.edit_profile_with_username", username=username))


@user_routes.route("/edit-profile/<username>", methods=["GET", "POST"])
def edit_profile_with_username(username):
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)
    user = User.query.filter_by(username=username).first()
    form = EditProfileForm(obj=user)
    if request.method == "POST":
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()
            flash("Ваши данные успешно обновлены!", "success")
            return redirect(url_for("user_routes.profile_with_username", username=username))
        else:
            flash("Проверьте Ваши данные!", "error")
    return render_template("user/edit_profile.html", menu=menu, form=form, user=user, username=username)
