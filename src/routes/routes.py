from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from __main__ import app, db
from models.models import User, Column, ContactMessage, Task, Board, validate_password, validate_name

menu = [
    {"name": "Главная", "url": "/", "page": "home"},
    {"name": "О нас", "url": "/about", "page": "about"},
    {"name": "Контакт", "url": "/contact", "page": "contact"},
    {"name": "Мои проекты", "url": "/profile/projects/", "page": "tasks"},
    {"name": "Профиль", "url": "/profile", "page": "profile"},
]

home_routes = Blueprint('home_routes', __name__)
about_routes = Blueprint('about_routes', __name__)
user_routes = Blueprint('user_routes', __name__)
page_error = Blueprint('404_routes', __name__)


@app.errorhandler(500)
def handle_500(err):
    return render_template('error/page500.html', menu=menu), 500

@app.errorhandler(401)
def handle_401(err):
    return render_template('error/page401.html', menu=menu), 401


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error/page404.html', menu=menu), 404


@home_routes.route('/')
def home():
    # print('sesiya dom: ', session['userLogged'])
    if not 'userLogged' in session:
        return render_template('home/index.html', menu=menu, page="home")
    if 'userLogged' in session:
        return redirect(url_for('user_routes.profile', username=session['userLogged']))


@about_routes.route('/about')
def about():
    return render_template('about/about.html', menu=menu, page='about')


@user_routes.route('/profile', methods=['GET'])
def profile():
    if 'userLogged' not in session:
        # flash('Вы не авторизованы', 'error')
        return redirect(url_for('home_routes.home'))
    username = session['userLogged']
    return redirect(url_for('user_routes.profile_with_username', username=username))


@user_routes.route('/profile/<username>')
def profile_with_username(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    user = User.query.filter_by(username=username).first()
    return render_template('user/profile.html', menu=menu, page='profile', user=user)

@user_routes.route('/logout')
def logout():
    session.pop('userLogged', None)
    flash('Вы успешно вышли из аккаунта', 'success')
    return redirect(url_for('home_routes.home', menu=menu, page="home"))


@user_routes.route('/profile/<username>/projects/<board_id>')
def tasks(board_id):
    board = Board.query.get(board_id)
    return render_template('user/projects.html', menu=menu, page="tasks", board=board)


@user_routes.route('/profile/edit')
def edit_profile():
    return render_template('user/profile.html', menu=menu, page='profile_edit')


@about_routes.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if validate_name(request.form['username']):
            name = request.form['name']
            email = request.form['email']
            message_text = request.form['message']
            if len(name) > 2 and email is not None and message_text is not None:
                message = ContactMessage(name=name, email=email, message=message_text)
                db.session.add(message)
                db.session.commit()
                flash('Сообщение отправлено.', 'success')
            else:
                flash('Проверьте ваши данные.', 'error')
    return render_template('about/contact.html', menu=menu, page='contact')


@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if validate_name(request.form['username']):
            username = request.form['username']
            password = request.form['password']
            password2 = request.form['password2']
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Пользователь с таким именем уже существует!', 'error')
                return redirect(url_for('user_routes.register', menu=menu))
            else:
                if password == password2:
                    if validate_password(password):
                        new_user = User(username=username, password=password)
                        db.session.add(new_user)
                        db.session.commit()
                        flash('Регистрация успешно завершена!', 'success')
                        return redirect(url_for('user_routes.login', menu=menu, page="home"))
                    else:
                        flash('''Пароль должен быть от 8-20 символов, содержать латинские хотя бы одну'''
                         '''заглавную и маленькую буквы, и хотя бы одну цирфру, хотя бы один спец символ!''', 'error')
                else:
                    flash('Проверьте правильность пароля!', 'error')
        else:
            flash('''Имя должно содержать от 3-16 символов, состоять только из заглавных и прописных букв латинского алфавита, может также содержать цирфры, и символы "_", "-"!''', 'error')
    return render_template('user/register.html', menu=menu)


@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('user_routes.profile', username=session['userLogged'])), 301

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['userLogged'] = username
            flash('Авторизация прошла успешно', 'success')
            return redirect(url_for('user_routes.profile', username=username))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')

    return redirect(url_for('user_routes.profile'))


@user_routes.route('/add_column', methods=['GET', 'POST'])
def add_column():
    data = request.form
    column_name = data['column_name']

    new_column = Column(name=column_name)

    db.session.add(new_column)
    db.session.commit()
    return redirect(url_for('index')), 200
