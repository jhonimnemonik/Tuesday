from flask import render_template
from __main__ import app, db

# from home_views import home_routes
# from about_views import about_routes
# from todo_views import todo_routes
# from user_views import user_routes


app = app
db = db
menu = [
    {"name": "Главная", "url": "/", "page": "home"},
    {"name": "О нас", "url": "/about", "page": "about"},
    {"name": "Контакт", "url": "/contact", "page": "contact"},
    {"name": "Мои проекты", "url": "/profile/projects/", "page": "board"},
    {"name": "Профиль", "url": "/profile", "page": "profile"},
]

@app.errorhandler(500)
def handle_500(err):
    return render_template("error/page500.html", menu=menu), 500


@app.errorhandler(401)
def handle_401(err):
    return render_template("error/page401.html", menu=menu), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error/page404.html", menu=menu, user=None), 404


