from flask import Blueprint, render_template,request

home_routes = Blueprint('home_routes', __name__)
about_routes = Blueprint('about_routes', __name__)
user_routes = Blueprint('user_routes', __name__)

@home_routes.route('/')
def home():
    return render_template('home/index.html', page="home")

@about_routes.route('/about')
def about():
    return render_template('about/about.html', page='about')

@user_routes.route('/profile/<id>')
def profile():#(id, path):
    # return f"Пользователь: {id}"#,{path}" #render_template('user/profile.html')
    return render_template('user/profile.html', page='profile')


@user_routes.route('/profile/projects')
def tasks():
    return render_template('user/projects.html', page="tasks")

@user_routes.route('/profile/edit')
def edit_profile():
    return render_template('user/profile.html', page='profile_edit')

@about_routes.route('/contact')
def contact():
    return render_template('about/contact.html', page='contact')


@user_routes.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        #сохранение данных пользователя в базу данных
        return render_template('base.html')#, content='Регистрация успешно завершена!')
    #не POST, возвращаем страницу входа
    return render_template('user/login.html')

@user_routes.route('/login', methods=['POST'])
def login():
    return render_template('user/login.html')

@user_routes.route('/add_column', methods=['POST'])
def add_column():
    # Получаем данные из запроса
    data = request.json
    column_name = data['column_name']

    # Ваш код для добавления столбца в базу данных здесь

    # Возвращаем успешный ответ
    return '', 200


