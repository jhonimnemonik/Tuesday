from flask import Blueprint, render_template, request, jsonify

from main import create_app

_, db = create_app()

menu = [
    {"name": "Главная", "url": "/", "page": "home"},
    {"name": "Мои проекты", "url": "/profile/projects", "page": "tasks"},
    {"name": "Контакт", "url": "/contact", "page": "contact"},
    {"name": "О нас", "url": "/about", "page": "about"},
    {"name": "Профиль", "url": "/profile/edit", "page": "profile_edit"}
]
    #{"name": "", "url": ""},


home_routes = Blueprint('home_routes', __name__)
about_routes = Blueprint('about_routes', __name__)
user_routes = Blueprint('user_routes', __name__)

@home_routes.route('/')
def home():
    return render_template('home/index.html', menu=menu, page="home")

@about_routes.route('/about')
def about():
    return render_template('about/about.html', menu=menu, page='about')

@user_routes.route('/profile/<id>')
def profile():#(id, path):
    # return f"Пользователь: {id}"#,{path}" #render_template('user/profile.html')
    return render_template('user/profile.html', menu=menu, page='profile')


@user_routes.route('/profile/projects')
def tasks():
    return render_template('user/projects.html', menu=menu, page="tasks")

@user_routes.route('/profile/edit')
def edit_profile():
    return render_template('user/profile.html', menu=menu, page='profile_edit')

@about_routes.route('/contact')
def contact():
    return render_template('about/contact.html', menu=menu, page='contact')


@user_routes.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        #сохранение данных пользователя в базу данных
        return render_template('base.html', menu=menu)#, content='Регистрация успешно завершена!')
    #не POST, возвращает страницу входа
    return render_template('user/login.html', menu=menu)

@user_routes.route('/login', methods=['GET','POST'])
def login():
    return render_template('user/login.html', menu=menu)

# @user_routes.route('/add_column', methods=['GET','POST'])
# def add_column():
#     if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
#         data = request.json
#         column_name = data['column_name']
#         #в БД
#         return jsonify({'message': 'Данные успешно обработаны'})
#     else:
#         return jsonify({'error': 'Unsupported media content type'}), 415
class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
@user_routes.route('/add_column', methods=['POST'])
def add_column():
    data = request.json
    column_name = data['column_name']

    new_column = Column(name=column_name)

    db.session.add(new_column)
    db.session.commit()

    return '', 200