from sqlite3 import IntegrityError
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, Blueprint
from flask_login import current_user
from sqlalchemy import insert
from forms.forms import BoardForm, TaskForm, ColumnForm, ContentForm
from models.models import User, Column, Task, Board, ChatMessage, ColumnContent
from views import db, menu, login_required, check_request_method, chk_user

todo_routes = Blueprint("todo_routes", __name__)


@todo_routes.route("/profile/<username>/projects/create-board", methods=["GET", "POST"])
@login_required
@check_request_method("GET", "POST")
def create_board(username):
    form = BoardForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=username).first()
            new_board = Board(name=form.name.data or None, user_id=user.id)
            db.session.add(new_board)
            db.session.commit()
            flash("Доска успешно создана!", "success")
            return redirect(url_for("todo_routes.board_get", username=username, board_id=new_board.id))
        else:
            flash("Пустое поле!", "error")
            return render_template("boards/create_board.html", menu=menu, page="create_board", form=form, username=username)
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
    if not board:
        flash("Доска не найдена.", "error")
        return redirect(url_for("user_routes.profile")), 301
    return render_template("user/projects.html", menu=menu, page="board", board=board, username=username)
# @todo_routes.route("/profile/<username>/projects/<int:board_id>", methods=["GET"])
# @login_required
# def board_get(username, board_id):
#     user_id, _ = chk_user()
#     if not username:
#         flash("Пользователь не найден.", "error")
#         return redirect(url_for("home_routes.home")), 301
#     # boards = Board.query.filter_by(username=username).all()
#     boards = Board.query.filter_by(user_id=user_id).all()
#     return render_template("user/projects.html", menu=menu, page="board", board=board, username=username)

#     board = Board.query.get(board_id)
#     return render_template("user/projects.html", menu=menu, page="board", board=board, username=username)
# def projects(username):
#     # Получите список досок из базы данных или любого другого источника данных
#     boards = Board.query.filter_by(username=username).all()
#     return render_template("user/projects.html", boards=boards, username=username)

# @todo_routes.route("/profile/<username>/projects/", methods=["GET"])
# def board(username):

#     else:
#         username = session["userLogged"]
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             flash("Пользователь не найден.", "error")
#             return redirect(url_for("home_routes.home")), 301
#         if not user.boards:
#             return redirect(url_for("todo_routes.create_board"))
#         if user:
#             boards = Board.query.filter_by(user_id=user.id).all()
#             if boards:
#                 for board in boards:
#                     board_id = board.id
#                 return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id, page='board'))
#             else:
#                 return redirect(url_for("todo_routes.board_create", username=username, board_id=board_id, page='board'))

@todo_routes.route("/profile/projects/", methods=["GET"])
@login_required
def board():
    username = session["userLogged"]
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Пользователь не найден.", "error")
        return redirect(url_for("home_routes.home"))
    if not user.boards:
        return redirect(url_for("todo_routes.create_board"))
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
                board_id=board_id
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id))
        else:
            flash("Не добавлено.", "error")
            return render_template("boards/new_task.html", form=form, username=username, board_id=board_id)
    return render_template("boards/new_task.html",menu=menu, form=form, username=username, board_id=board_id)


@todo_routes.route("/profile/<username>/projects/<int:board_id>/add_column", methods=["GET", "POST"])
@login_required
def add_column(username, board_id):
    if request.method == "GET":
        return render_template("boards/column_create.html", menu=menu, page="home", username=username, board_id=board_id)
    if request.method == "POST":
        column_name = request.form.get("column_name")
        try:
            stmt = insert(Column).values(name=column_name, board_id=board_id)
            db.session.execute(stmt)
            db.session.commit()
            return redirect(url_for("todo_routes.board"))
        except IntegrityError as e:
            db.session.rollback()
            flash(f"An error occurred: {e}")
            return abort(500)
    else:
        flash("Method not allowed")
        return abort(405)


@todo_routes.route("/profile/<username>/projects/<int:board_id>/add_content/<int:task_id>/<int:column_id>",
                   methods=["GET", "POST"])
@login_required
def add_content(board_id, task_id, column_id, username):
    form = ContentForm()
    if request.method == "GET":
        return render_template("boards/add_column_content.html", menu=menu, page="home", username=username, board_id=board_id, form=form)
    if request.method == "POST":

        if form.validate_on_submit():
            content = form.content.data
            try:
                new_content = ColumnContent(content=content, task_id=task_id, column_id=column_id)
                db.session.add(new_content)
                db.session.commit()
                flash("Контент успешно добавлен!", "success")
                return redirect(url_for("todo_routes.board_get", username=session["userLogged"], board_id=board_id))
            except Exception as e:
                flash(f"Ошибка при добавлении контента: {str(e)}", "error")
                return redirect(url_for("todo_routes.board_get", username=session["userLogged"], board_id=board_id))

    return render_template("boards/add_column_content.html", form=form, username=session["userLogged"], menu=menu)


@todo_routes.route("/task/<int:task_id>/messages", methods=["GET"])
def get_task_messages(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    messages = task.messages.order_by(ChatMessage.timestamp.desc()).all()
    return jsonify([message.serialize() for message in messages])


@todo_routes.route("/task/<int:task_id>/messages", methods=["POST"])
def create_task_message(task_id):
    data = request.json
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    new_message = ChatMessage(task_id=task_id, sender_id=current_user.id, text=data["text"])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.serialize()), 201
