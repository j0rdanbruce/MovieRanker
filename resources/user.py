import json

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import render_template, flash, redirect, url_for, session, request
from forms import RegistrationForm, LoginForm

from db import mysql
from models.user import User

#from schemas import PlainUserSchema

blp = Blueprint("user", __name__, description="operations for login")

@blp.route("/register", methods=["POST", "GET"])
#register for an account
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, pswrd=form.password1.data)
        #user.set_password(form.password1.data)
        user.insert_user(form.fname.data, form.lname.data)
        return redirect(url_for("user.login_here"))
    return render_template("registration.html", form=form)
#login to your account
@blp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, pswrd=form.password.data)
        user.add_to_session()
        if user.is_authenticated():
            return redirect(url_for("user.home_page"))
        flash("Incorrect username or password")
    return render_template("login.html", form=form)
#logout of your account
@blp.route("/logout", methods=["GET"])
def logout():
    session["id"] = None
    return redirect(url_for("user.login"))

#returns home page of the logged in user
@blp.route("/home", methods=["GET"])
def home_page():
    cur = mysql.connection.cursor()
    query = "SELECT username FROM user WHERE id={}".format(int(session["id"]))
    cur.execute(query)
    data = cur.fetchone()
    cur.close()
    return render_template("home_page.html", username=data['username'])


'''@blp.route("/users")
class User(MethodView):
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users'''

@blp.route('/database')
def index():
    cur = mysql.connection.cursor()
    query = "CREATE TABLE  IF NOT EXISTS Person (id INT PRIMARY KEY, LastName VARCHAR(25))"
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return 'done'