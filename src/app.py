from flask import Flask
from config.config import Config
from db.db import create_db
from flask_socketio import SocketIO


# import os
# app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app = Flask(__name__)
app.config.from_object(Config)
db, migrate = create_db(app)
socketio = SocketIO(app)


if __name__ == "__main__":
    # from views import home_routes, user_routes, about_routes, todo_routes

    from views.home_views import home_routes
    from views.about_views import about_routes
    from views.todo_views import todo_routes
    from views.user_views import user_routes

    app.register_blueprint(home_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(about_routes)
    app.register_blueprint(todo_routes)
    app.run(debug=True)

    # socketio.run(app, log_output=True, use_reloader=True, debug=True)
