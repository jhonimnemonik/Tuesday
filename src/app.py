from flask import Flask
from db.db import create_db
from flask_socketio import SocketIO


app = Flask(__name__)
app.config.from_pyfile("config.py")
db, migrate = create_db(app)
socketio = SocketIO(app)


if __name__ == "__main__":
    from views.home_views import home_routes
    from views.about_views import about_routes
    from views.todo_views import todo_routes
    from views.user_views import user_routes

    app.register_blueprint(home_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(about_routes)
    app.register_blueprint(todo_routes)

    socketio.run(app, log_output=True, use_reloader=True, debug=True, allow_unsafe_werkzeug=True)
