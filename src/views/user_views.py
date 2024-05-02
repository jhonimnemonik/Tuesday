from flask import render_template, request, redirect, url_for, flash, session, abort, Blueprint
from forms.forms import EditProfileForm
from models.models import User, Board
from views import db, menu, login_required, chk_user

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/profile", methods=["GET"])
def profile():
    if "userLogged" in session:
        username = session["userLogged"]
        return redirect(url_for("user_routes.profile_with_username", username=username))
    else:
        flash("Ваши данные некорректны", "error")
        return redirect(url_for("home_routes.register"))


@user_routes.route("/profile/<username>")
@login_required
def profile_with_username(username):
    user = chk_user()[2]
    if not user:
        abort(404)
    user_boards = Board.query.filter_by(user_id=user.id).all()
    other_boards = Board.query.filter(Board.user_id != user.id).all()
    accessible_boards = []
    c = 0
    for board in other_boards:
        c += 1
        print(c)
        print(user.has_access_to_board(board))
        if user.has_access_to_board(board):
            accessible_boards.append(board)

    return render_template(
        "user/profile.html",
        menu=menu,
        page="profile",
        user=user,
        username=username,
        user_boards=user_boards,
        other_boards=accessible_boards,
    )


@user_routes.route("/profile/info", methods=["GET"])
@login_required
def profile_info():
    user_id, username, user = chk_user()
    if user.boards:
        boards = Board.query.all()
        if boards:
            for board in boards:
                board_id = board.id
    return redirect(url_for("user_routes.profile_info_get", username=username, board_id=board_id))


@user_routes.route("/profile/<username>/info", methods=["GET"])
@login_required
def profile_info_get(username):
    username = chk_user()[1]
    user = User.query.filter_by(username=username).first()
    return render_template("user/user_info.html", menu=menu, page="profile", user=user, username=username)


@user_routes.route("/edit-profile", methods=["GET"])
@login_required
def edit_profile(username):
    if "userLogged" not in session:
        flash("Вы не авторизованы.", "error")
        return redirect(url_for("home_routes.home"))
    username = session["userLogged"]
    return redirect(url_for("user_routes.edit_profile_with_username", username=username))


@user_routes.route("/edit-profile/<username>", methods=["GET", "POST"])
@login_required
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
