from flask import render_template, request, flash, session, Blueprint
from models.models import ContactMessage
from sqlalchemy.sql import text
from views import db, menu

about_routes = Blueprint("about_routes", __name__)

@about_routes.route("/about")
def about():
    return render_template("about/about.html", menu=menu, page="about")


@about_routes.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message_text = request.form["message"]
        is_valid, error_message = ContactMessage.validate_data(email, name)
        if not is_valid:
            flash(error_message, "error")
        else:
            if len(message_text) < 3:
                flash("Слишком короткое сообщение.", "error")
            else:
                query = text("INSERT INTO contact_message (name, email, message) VALUES (:name, :email, :message)")
                db.session.execute(query, {"name": name, "email": email, "message": message_text})
                db.session.commit()
                flash(error_message, "success")
    if "userLogged" in session:
        return render_template("about/contact.html", menu=menu, page="contact", user=session["userLogged"])
    else:
        return render_template("about/contact.html", menu=menu, page="contact")
