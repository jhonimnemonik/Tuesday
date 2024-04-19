# from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, jsonify
# from __main__ import app, db
# from flask_login import current_user
# from forms.forms import EditProfileForm, CreateBoardForm, TaskForm
# from models.models import User, Column, ContactMessage, Task, Board, ChatMessage
# from sqlalchemy.sql import text
#
#
# menu = [
#     {"name": "Главная", "url": "/", "page": "home"},
#     {"name": "О нас", "url": "/about", "page": "about"},
#     {"name": "Контакт", "url": "/contact", "page": "contact"},
#     {"name": "Мои проекты", "url": "/profile/projects/", "page": "board"},
#     {"name": "Профиль", "url": "/profile", "page": "profile"},
# ]
#
# home_routes = Blueprint("home_routes", __name__)
# about_routes = Blueprint("about_routes", __name__)
# user_routes = Blueprint("user_routes", __name__)
# todo_routes = Blueprint("todo_routes", __name__)
#
#
# @app.errorhandler(500)
# def handle_500(err):
#     return render_template("error/page500.html", menu=menu), 500
#
#
# @app.errorhandler(401)
# def handle_401(err):
#     return render_template("error/page401.html", menu=menu), 401
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template("error/page404.html", menu=menu, user=None), 404
#
#
# @home_routes.route("/")
# def home():
#     if not "userLogged" in session:
#         return render_template("home/index.html", menu=menu, page="home", user=None)
#     if "userLogged" in session:
#         return redirect(url_for("user_routes.profile", username=session["userLogged"]))
#
#
# @about_routes.route("/about")
# def about():
#     return render_template("about/about.html", menu=menu, page="about")
#
#
# @about_routes.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         name = request.form["name"]
#         email = request.form["email"]
#         message_text = request.form["message"]
#         is_valid, error_message = ContactMessage.validate_data(email, name)
#         if not is_valid:
#             flash(error_message, "error")
#         else:
#             if len(message_text) < 3:
#                 flash("Слишком короткое сообщение.", "error")
#             else:
#                 query = text("INSERT INTO contact_message (name, email, message) VALUES (:name, :email, :message)")
#                 db.session.execute(query, {"name": name, "email": email, "message": message_text})
#                 db.session.commit()
#                 flash(error_message, "success")
#     if "userLogged" in session:
#         return render_template("about/contact.html", menu=menu, page="contact", user=session["userLogged"])
#     else:
#         return render_template("about/contact.html", menu=menu, page="contact")
#
#
# @user_routes.route("/profile", methods=["GET"])
# def profile():
#     if "userLogged" not in session:
#         flash("Вы не авторизованы.", "error")
#         return redirect(url_for("home_routes.home"))
#     username = session["userLogged"]
#     return redirect(url_for("user_routes.profile_with_username", username=username))
#
#
# @user_routes.route("/profile/<username>")
# def profile_with_username(username):
#     if "userLogged" not in session or session["userLogged"] != username:
#         abort(401)
#     user = User.query.filter_by(username=username).first()
#     return render_template("user/profile.html", menu=menu, page="profile", user=user, username=username)
#
#
# @user_routes.route("/profile/info", methods=["GET"])
# def profile_info():
#     if "userLogged" not in session:
#         flash("Вы не авторизованы.", "error")
#         return redirect(url_for("home_routes.home"))
#     username = session["userLogged"]
#     return redirect(url_for("user_routes.profile_info_get", username=username))
#
#
# @user_routes.route("/profile/<username>/info", methods=["GET"])
# def profile_info_get(username):
#     if "userLogged" not in session or session["userLogged"] != username:
#         abort(401)
#     user = User.query.filter_by(username=username).first()
#     return render_template("user/user_info.html", menu=menu, page="profile", user=user)
#
#
# @todo_routes.route("/create-board", methods=["GET", "POST"])
# def create_board():
#     form = CreateBoardForm()
#     if form.validate_on_submit():
#         username = session["userLogged"]
#         user = User.query.filter_by(username=username).first()
#         if form.name.data:
#             new_board = Board(name=form.name.data, user_id=user.id)
#         else:
#             new_board = Board(user_id=user.id)
#         db.session.add(new_board)
#         db.session.commit()
#         board_id = Board.query.filter_by(name=form.name.data).first()
#         flash("Доска успешно создана!", "success")
#         return redirect(url_for("user_routes.board_get", username=username, board_id=board_id.id))
#     return render_template(
#         "boards/create_board.html", menu=menu, page="create_board", form=form, user=session["userLogged"]
#     )
#
#
# @todo_routes.route("/profile/<username>/projects/<int:board_id>", methods=["GET", "POST"])
# def board_get(username, board_id):
#     if "userLogged" not in session or session["userLogged"] != username:
#         return abort(401)
#     if board_id == None:
#         return redirect(url_for("user_routes.create_board", username=username)), 301
#     board = Board.query.get(board_id)
#     return render_template("user/projects.html", menu=menu, page="board", board=board, user=session["userLogged"])
#
#
# @todo_routes.route("/profile/projects/", methods=["GET"])
# def board():
#     if "userLogged" not in session:
#         flash("Вы не авторизованы.", "error")
#         return redirect(url_for("home_routes.home"))
#
#     username = session["userLogged"]
#     user = User.query.filter_by(username=username).first()
#
#     if not user:
#         flash("Пользователь не найден.", "error")
#         return redirect(url_for("home_routes.home"))
#
#     if not user.boards:
#         return redirect(url_for("user_routes.create_board"))
#     print(user)
#     if user:
#         boards = Board.query.all()
#         if boards:
#             for board in boards:
#                 board_id = board.id
#         return redirect(url_for("user_routes.board_get", username=username, board_id=board_id, page='board'))
#
#
# @todo_routes.route("/create_task", methods=["GET", "POST"])
# def create_task():
#     form = TaskForm()
#     if form.validate_on_submit():
#         new_task = Task(
#             name=form.name.data,
#             status=form.status.data,
#             priority=form.priority.data,
#             description=form.description.data,
#             board_id=form.board_id.data,
#         )
#         db.session.add(new_task)
#         db.session.commit()
#         return redirect(url_for("user_routes.board"))
#     return render_template("boards/new_task.html", form=form, user=session["userLogged"])
#
#
# @user_routes.route("/add_column", methods=["GET", "POST"])
# def add_column():
#     if request.method == "GET":
#         return
#     if request.method == "POST":
#         print("1")
#         column_name = request.form.get("column_name")
#         if column_name:
#             print("2")
#             new_column = Column(name=column_name)
#             db.session.add(new_column)
#             db.session.commit()
#             return redirect(url_for("user_routes.board"))
#         else:
#             return "Name of column is missing", 400
#     else:
#         return "Method not allowed", 405
#
#
# @user_routes.route("/edit-profile", methods=["GET"])
# def edit_profile():
#     if "userLogged" not in session:
#         flash("Вы не авторизованы.", "error")
#         return redirect(url_for("home_routes.home"))
#     username = session["userLogged"]
#     return redirect(url_for("user_routes.edit_profile_with_username", username=username))
#
#
# @user_routes.route("/edit-profile/<username>", methods=["GET", "POST"])
# def edit_profile_with_username(username):
#     if "userLogged" not in session or session["userLogged"] != username:
#         abort(401)
#     user = User.query.filter_by(username=username).first()
#     form = EditProfileForm(obj=user)
#     if request.method == "POST":
#         if form.validate_on_submit():
#             user.username = form.username.data
#             user.email = form.email.data
#             db.session.commit()
#             flash("Ваши данные успешно обновлены!", "success")
#             return redirect(url_for("user_routes.edit_profile_with_username", username=username))
#         else:
#             flash("Проверьте Ваши данные!", "error")
#     return render_template("user/edit_profile.html", menu=menu, form=form, user=user)
#
#
# @user_routes.route("/login", methods=["GET", "POST"])
# def login():
#     if "userLogged" in session:
#         return redirect(url_for("user_routes.profile", username=session["userLogged"])), 301
#
#     elif request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         user = User.query.filter_by(username=username).first()
#
#         if user and user.check_password(password):
#             session["userLogged"] = username
#             flash(f"Авторизация прошла успешно. Приветствуем {username}!", "success")
#             return redirect(url_for("user_routes.profile", username=username))
#         else:
#             flash("Неправильное имя пользователя или пароль", "error")
#
#     return redirect(url_for("user_routes.profile"))
#
#
# @user_routes.route("/logout")
# def logout():
#     session.pop("userLogged", None)
#     flash("Вы успешно вышли из аккаунта", "success")
#     return redirect(url_for("home_routes.home", menu=menu, page="home"))
#
#
# @user_routes.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]
#         password2 = request.form["password2"]
#         is_valid, error_message = User.validate_registration(username, password, password2, email)
#         if not is_valid:
#             flash(error_message, "error")
#             return render_template("user/register.html", menu=menu)
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             flash("Пользователь с таким именем уже существует!", "error")
#             return redirect(url_for("user_routes.register", menu=menu))
#         else:
#             new_user = User(username=username, password=password, email=email)
#             db.session.add(new_user)
#             db.session.commit()
#             flash(error_message, "success")
#             return redirect(url_for("user_routes.login", menu=menu, page="home"))
#
#     return render_template("user/register.html", menu=menu, user=None)
#
#
# @app.route("/task/<int:task_id>/messages", methods=["GET"])
# def get_task_messages(task_id):
#     task = Task.query.get(task_id)
#     if not task:
#         return jsonify({"error": "Task not found"}), 404
#
#     messages = task.messages.order_by(ChatMessage.timestamp.desc()).all()
#     return jsonify([message.serialize() for message in messages])
#
#
# @app.route("/task/<int:task_id>/messages", methods=["POST"])
# def create_task_message(task_id):
#     data = request.json
#     task = Task.query.get(task_id)
#     if not task:
#         return jsonify({"error": "Task not found"}), 404
#
#     new_message = ChatMessage(task_id=task_id, sender_id=current_user.id, text=data["text"])
#     db.session.add(new_message)
#     db.session.commit()
#     return jsonify(new_message.serialize()), 201
