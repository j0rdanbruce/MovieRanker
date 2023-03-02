import json

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import render_template, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, login_required, logout_user

from db import db
from models import UserModel

from schemas import PlainUserSchema

blp = Blueprint("user", __name__, description="operations for login")

@blp.route("/register", methods=["POST", "GET"])
#register for an account
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserModel(username=form.username.data, email=form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user.login"))
    return render_template("registration.html", form=form)
#login to your account
@blp.route("/login", methods=["POST", "GET"])
def login_here():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('user.home_page'))
        flash("Incorrect username or password")
    return render_template("login.html", form=form)
#logout of your account
@blp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))

#returns home page of the logged in user
@blp.route("/home", methods=["GET"])
def home_page():
    return render_template("home_page.html")


'''@blp.route("/users")
class User(MethodView):
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users'''