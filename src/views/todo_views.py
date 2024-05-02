from datetime import datetime
from sqlite3 import IntegrityError
from flask import render_template, request, redirect, url_for, flash, abort, jsonify, Blueprint
from sqlalchemy import insert
from forms.forms import BoardForm, TaskForm, ContentForm, TeamUserForm
from models.models import User, Column, Task, Board, ChatMessage, ColumnContent, TeamUser
from views import db, menu, login_required, chk_user
from sqlalchemy import or_

todo_routes = Blueprint("todo_routes", __name__)


@todo_routes.route("/profile/<username>/projects/create-board", methods=["GET", "POST"])
@login_required
def create_board(username):
    form = BoardForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=username).first()
            new_board = Board(name=form.name.data, user_id=user.id, team_user_id=None)
            db.session.add(new_board)
            db.session.commit()
            flash("Доска успешно создана!", "success")
            return redirect(url_for("todo_routes.board_get", username=username, board_id=new_board.id))
        else:
            flash("Пустое поле!", "error")
            return render_template(
                "boards/create_board.html", menu=menu, page="create_board", form=form, username=username
            )
    return render_template("boards/create_board.html", menu=menu, page="create_board", form=form, username=username)


@todo_routes.route("/profile/<username>/projects/<int:board_id>/delete", methods=["POST"])
@login_required
def delete_board(username, board_id):
    board = Board.query.get(board_id)
    if not board:
        flash("Доска не найдена.", "error")
        return redirect(url_for("todo_routes.board"))
    db.session.delete(board)
    db.session.commit()
    flash("Доска успешно удалена.", "success")
    return redirect(url_for("user_routes.profile", username=username))


@todo_routes.route("/profile/<username>/projects/<int:board_id>", methods=["GET"])
@login_required
def board_get(username, board_id):
    user = User.query.filter_by(username=username).first()
    board = Board.query.filter_by(id=board_id, user_id=user.id).first()
    team_users = TeamUser.query.filter_by(board_id=board_id).all()
    if not board:
        flash("Доска не найдена.", "error")
        return redirect(url_for("user_routes.profile")), 301
    return render_template(
        "user/projects.html",
        team_users=team_users,
        menu=menu,
        page="board",
        user=user,
        board=board,
        board_id=board_id,
        username=username,
    )


@todo_routes.route("/shared-board/<username>/<int:board_id>")
@login_required
def shared_board(username, board_id):
    current_user_id, current_username, current_user = chk_user()

    if not current_user:
        flash("Пользователь не найден.", "error")
        return redirect(url_for("home_routes.home"))

    if current_username != username:
        flash("Доступ разрешен только собственной информации.", "error")
        return redirect(url_for("user_routes.profile"))

    board = Board.query.get(board_id)
    print("board.id", board.id)
    if not board:
        flash("Доска не найдена.", "error")
        return redirect(url_for("user_routes.profile"))

    team_user = None
    for tu in board.team_users:
        if str(tu.username) == str(current_user.username):
            team_user = tu
            break

    if not team_user:
        flash("У вас нет доступа к этой доске.", "error")
        abort(403)

    tasks = Task.query.filter_by(board_id=board.id).all()
    columns = Column.query.filter_by(board_id=board.id).all()

    return render_template(
        "boards/shared_board.html",
        board=board,
        board_id=board_id,
        tasks=tasks,
        columns=columns,
        username=username,
        menu=menu,
    )


@todo_routes.route("/profile/projects/", methods=["GET"])
def board():
    user_id, username, user = chk_user()
    if not user:
        flash("Пользователь не найден.", "error")
        return redirect(url_for("home_routes.home"))
    if not user.boards:
        return redirect(url_for("todo_routes.create_board", username=username))
    first_board_id = user.boards[0].id
    return redirect(url_for("todo_routes.board_get", username=username, board_id=first_board_id))


@todo_routes.route("/profile/<username>/projects/<int:board_id>/create-task", methods=["GET", "POST"])
@login_required
def create_task(username, board_id):
    form = TaskForm()

    if request.method == "POST":
        form.board_id.data = board_id
        print(form.validate_on_submit())
        if form.validate_on_submit():
            print(board_id)
            new_task = Task(
                name=form.name.data,
                status=form.status.data,
                priority=form.priority.data,
                description=form.description.data,
                board_id=board_id,
            )
            db.session.add(new_task)
            db.session.commit()
            flash("Задача успешно добавлена.", "success")
            return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id))
        else:
            flash("Не добавлено.", "error")
            return render_template("boards/new_task.html", form=form, username=username, board_id=board_id)
    return render_template("boards/new_task.html", menu=menu, form=form, username=username, board_id=board_id)


@todo_routes.route("/profile/<username>/projects/<int:board_id>/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(username, board_id, task_id):
    task = Task.query.get(task_id)
    if not task:
        flash("Задача не найдена.", "error")
        return redirect(url_for("todo_routes.board", username=username, board_id=board_id))
    db.session.delete(task)
    db.session.commit()
    flash("Задача успешно удалена.", "success")
    return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id))


@todo_routes.route("/profile/<username>/projects/<int:board_id>/add_column", methods=["GET", "POST"])
@login_required
def add_column(username, board_id):
    if request.method == "GET":
        return render_template(
            "boards/column_create.html", menu=menu, page="home", username=username, board_id=board_id
        )
    if request.method == "POST":
        column_name = request.form.get("column_name")
        try:
            stmt = insert(Column).values(name=column_name, board_id=board_id)
            db.session.execute(stmt)
            db.session.commit()
            flash("Колонка добавлена.", "success")
            return redirect(url_for("todo_routes.board", board_id=board_id, username=username, menu=menu))
        except IntegrityError as e:
            db.session.rollback()
            flash(f"An error occurred: {e}")
            return abort(500)
    else:
        flash("Method not allowed")
        return abort(405)


@todo_routes.route(
    "/profile/<username>/projects/<int:board_id>/add_content/<int:task_id>/<int:column_id>", methods=["GET", "POST"]
)
@login_required
def add_content(board_id, task_id, column_id, username):
    form = ContentForm()
    if request.method == "GET":
        return render_template(
            "boards/add_column_content.html", menu=menu, page="home", username=username, board_id=board_id, form=form
        )
    if request.method == "POST":
        username = chk_user()[1]
        if form.validate_on_submit():
            content = form.content.data
            try:
                new_content = ColumnContent(content=content, task_id=task_id, column_id=column_id)
                db.session.add(new_content)
                db.session.commit()
                flash("Контент успешно добавлен!", "success")
                return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id))
            except Exception as e:
                flash(f"Ошибка при добавлении контента: {str(e)}", "error")
                return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id))

    return render_template("boards/add_column_content.html", form=form, username=username, menu=menu, board_id=board_id)


@todo_routes.route("/profile/<username>/projects/<int:board_id>/add-user", methods=["GET", "POST"])
@login_required
def add_tuser(username, board_id):
    owner_name = chk_user()[1]
    user_own = User.query.filter_by(username=owner_name).first()
    usr_own_email = user_own.email
    form = TeamUserForm()

    if request.method == "POST":
        if form.validate_on_submit():
            name_or_email = form.name_or_email.data
            if name_or_email != owner_name and name_or_email != usr_own_email:
                user = User.query.filter(or_(User.username == name_or_email, User.email == name_or_email)).first()
                if user:
                    board = Board.query.get(board_id)
                    if board is not None:
                        existing_team_user = TeamUser.query.filter_by(
                            username=user.username, owner=user_own, board_id=board_id
                        ).first()

                        if existing_team_user:
                            flash("Пользователь уже в команде.", "error")
                        else:
                            new_team_user = TeamUser(username=user.username, owner=user_own, board_id=board_id)
                            db.session.add(new_team_user)
                            db.session.commit()
                            flash("Пользователь успешно добавлен в команду.", "success")
                            return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id))
                    else:
                        flash("Доска не найдена.", "error")
                else:
                    flash("Пользователь с таким именем или адресом электронной почты не найден.", "error")
            else:
                flash("Вы не можете добавить себя в команду.", "error")
        else:
            flash("Пожалуйста, проверьте введенные данные.", "error")

    return render_template("boards/add_user_team.html", form=form, menu=menu, username=username, board_id=board_id)


@todo_routes.route("/profile/<username>/projects/<int:board_id>/remove-user", methods=["GET", "POST"])
@login_required
def remove_user_from_board(username, board_id):
    if request.method == "POST":
        user_to_remove_name = request.form.get("username")
        board = Board.query.get(board_id)

        if board is None:
            flash("Доска не найдена.", "error")
            return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id))

        team_user_to_remove = TeamUser.query.filter_by(username=user_to_remove_name, board_id=board_id).first()

        if team_user_to_remove:
            db.session.delete(team_user_to_remove)
            db.session.commit()
            flash("Пользователь успешно удален из команды.", "success")
        else:
            flash("Пользователь не найден в команде данной доски.", "error")
        return redirect(url_for("todo_routes.remove_user_from_board", username=username, board_id=board_id))
    else:
        team_users = TeamUser.query.filter_by(board_id=board_id).all()
        return render_template(
            "boards/delete_user_team.html", menu=menu, username=username, board_id=board_id, team_users=team_users
        )


@todo_routes.route("/get-chat/<int:task_id>", methods=["GET"])
def get_chat(task_id):
    username = chk_user()[1]
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    messages = task.messages.order_by(ChatMessage.timestamp.desc()).all()
    return render_template("boards/chat_page.html", task=task, menu=menu, username=username, messages=messages)


@todo_routes.route("/add-chat/<int:task_id>/messages", methods=["POST"])
def add_chat_message(task_id):
    current_user = chk_user()[2]
    data = request.json
    print("data", data)
    new_message = ChatMessage(
        task_id=task_id, sender=current_user, sender_id=current_user.id, text=data["text"], timestamp=datetime.utcnow()
    )
    print("new_message", new_message)
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.serialize()), 201
