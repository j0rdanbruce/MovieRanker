from flask_smorest import Blueprint
from flask.views import MethodView
from flask import render_template, flash, redirect, url_for
from forms import RegistrationForm

from db import db
from models import UserModel

blp = Blueprint("user", __name__, description="operations for login")

@blp.route("/register", methods=["POST", "GET"])
#register for an account
def post():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserModel(username=form.username.data, email=form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user.LoginUser"))
    return render_template("registration.html", form=form)

@blp.route("/login")
class LoginUser(MethodView):
    def get(self):
        return render_template("login.html")