from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, Blueprint
from flask_login import current_user
from forms.forms import CreateBoardForm, TaskForm
from models.models import User, Column, Task, Board, ChatMessage
from views import db, menu

todo_routes = Blueprint("todo_routes", __name__)


@todo_routes.route("/create-board", methods=["GET", "POST"])
def create_board():
    form = CreateBoardForm()
    if form.validate_on_submit():
        username = session["userLogged"]
        user = User.query.filter_by(username=username).first()
        if form.name.data:
            new_board = Board(name=form.name.data, user_id=user.id)
        else:
            new_board = Board(user_id=user.id)
        db.session.add(new_board)
        db.session.commit()
        board_id = Board.query.filter_by(name=form.name.data).first()
        flash("Доска успешно создана!", "success")
        return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id.id))
    return render_template(
        "boards/create_board.html", menu=menu, page="create_board", form=form, user=session["userLogged"]
    )


@todo_routes.route("/profile/<username>/projects/<int:board_id>", methods=["GET", "POST"])
def board_get(username, board_id):
    if "userLogged" not in session or session["userLogged"] != username:
        return abort(401)
    if board_id is None:
        return redirect(url_for("todo_routes.create_board", username=username)), 301
    if board_id:
        board = Board.query.get(board_id)
    return render_template("user/projects.html", menu=menu, page="board", board=board, user=username)


@todo_routes.route("/profile/projects/", methods=["GET"])
def board():
    if "userLogged" not in session:
        flash("Вы не авторизованы.", "error")
        return redirect(url_for("home_routes.home")), 301
    if session["userLogged"]:
        username = session["userLogged"]
        user = User.query.filter_by(username=username).first()
    if not user:
        flash("Пользователь не найден.", "error")
        return redirect(url_for("home_routes.home")), 301
    if not user.boards:
        return redirect(url_for("todo_routes.create_board"))
    if user:
        boards = Board.query.all()
        if boards:
            for board in boards:
                board_id = board.id
        return redirect(url_for("todo_routes.board_get", username=username, board_id=board_id, page='board'))


@todo_routes.route("/create_task", methods=["GET", "POST"])
def create_task():
    if "userLogged" not in session:
        flash("Вы не авторизованы.", "error")
        return redirect(url_for("home_routes.home")), 301
    if "userLogged" in session:
        form = TaskForm()
        if form.validate_on_submit():
            new_task = Task(
                name=form.name.data,
                status=form.status.data,
                priority=form.priority.data,
                description=form.description.data,
                board_id=form.board_id.data,
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("todo_routes.board"))
    return render_template("boards/new_task.html", form=form, user=session["userLogged"])


@todo_routes.route("/add_column", methods=["GET", "POST"])
def add_column():
    if "userLogged" not in session:
        flash("Вы не авторизованы.", "error")
        return redirect(url_for("home_routes.home")), 301
    if "userLogged" in session:
        if request.method == "GET":
            return render_template("boards/column_create.html", menu=menu, page="home", user=None)
        if request.method == "POST":
            print("1")
            column_name = request.form.get("column_name")
            if column_name:
                print("2")
                new_column = Column(name=column_name)
                db.session.add(new_column)
                db.session.commit()
                return redirect(url_for("user_routes.board"))
            else:
                return "Name of column is missing", 400
    else:
        return "Method not allowed", 405


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
