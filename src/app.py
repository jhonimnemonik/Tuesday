from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    from routes.routes import home_routes, about_routes, user_routes
    app = Flask(__name__)
    app.register_blueprint(home_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(about_routes)
    return app




if __name__ == '__main__':
    app, db = create_app()
    app.run(debug=True)




######v2.0
# app = Flask(__name__)
# app.config.from_object('config.config.Config')
#
# app.register_blueprint(home_routes)
# app.register_blueprint(user_routes)
# app.register_blueprint(about_routes)
#
# if __name__ == '__main__':
#     app.run(debug=True)




######v1.0
# from flask import Flask, render_template, url_for, request
# # from src.controllers import home
#
#
# app = Flask(__name__)
# app.config.from_object('config.config.Config')
#
# # print(f"SECRET_KEY: {app.config['SECRET_KEY']}")
# # print(f"DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
# # print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
# # print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
#
#
# @app.route('/')
# def home():
#     print(url_for('home'))
#     return render_template('home/index.html', page="home")
#
#
# @app.route('/projects')
# def tasks():
#     print(url_for('tasks'))
#     return render_template('user/projects.html', page="tasks")
#
#
# @app.route('/about')
# def about():
#     print(url_for('about'))
#     return render_template('about/about.html', page='about')
#
#
# @app.route('/profile/<id>')
# def profile(id):#, path):
#     # return f"Пользователь: {id}"#,{path}" #render_template('user/profile.html')
#     return render_template('user/profile.html', page='profile')
#
#
# @app.route('/profile/edit')
# def edit_profile():
#     return render_template('user/profile.html', page='profile_edit')#edit_profile.html')
#
#
#
# @app.route('/contact')#, methods=['POST'])
# def contact():
#     # if request.method == 'POST':
#     #     name = request.form['name']
#     #     email = request.form['email']
#     #     message = request.form['message']
#     #     return 'Форма успешно отправлена!'
#
#     return render_template('about/contact.html', page='contact')
#
#
# @app.route('/register', methods=['POST'])
# def register():
#     return 'Регистрация успешно завершена!'
#
#
# @app.route('/login', methods=['POST'])
# def login():
#     return render_template('user/login.html')
#
# @app.route('/add_column', methods=['POST'])
# def add_column():
#     data = request.json
#     column_name = data['column_name']
#
#     #код для добавления в бд
#
#     #ответ
#     return '', 200
#
#
# # with app.test_request_context():
# #     # print( url_for('edit_profile'))
# #     print( url_for('profile', id='123'))
#
# if __name__ == '__main__':
#     app.run(debug=True)
