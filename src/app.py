import os
from flask import Flask
from db.db import create_db


app = Flask(__name__)
app.config.from_object('config.config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db, migarte = create_db(app)


if __name__ == '__main__':
    from routes.routes import home_routes, user_routes, about_routes, page_error
    app.register_blueprint(home_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(about_routes)
    app.register_blueprint(page_error)
    app.run(debug=True)
