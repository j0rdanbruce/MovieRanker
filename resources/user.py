from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import render_template, flash, redirect, url_for, session
from forms import RegistrationForm, LoginForm, EditUserForm

from db import mysql
from models.user import User
#wrapper functions here
from wrappers import login_required
import random

blp = Blueprint("user", __name__, description="operations for login")

@blp.route("/register", methods=["POST", "GET"])
#register for an account
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, pswrd=form.password1.data)
        #user.set_password(form.password1.data)
        user.insert_user(form.fname.data, form.lname.data)
        return redirect(url_for("user.login"))
    return render_template("registration.html", form=form)

#login to your account
@blp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, pswrd=form.password.data)
        user.add_to_session()
        if user.is_authenticated():
            return redirect(url_for("movies.search_movie", login_message="success"))
        else:
            flash("Incorrect username or password")
    message = request.args.get("logout_msg")
    if message:
        alert_msg = {}
        alert_msg["type"] = message
        alert_msg["message"] = "Come again soon!"
        return render_template("login.html", form=form, alert_message=alert_msg)
    return render_template("login.html", form=form)

#login as a guest user
@blp.route("/guest_login", methods=["GET"])
def login_guest():
    '''cursor = mysql.connection.cursor()
    rand_id = random.randint(1, 10000)
    exist_query = "SELECT EXISTS(SELECT * FROM user WHERE id={}) AS user_exists".format(rand_id)
    cursor.execute(exist_query)
    result = cursor.fetchone()
    while (result["user_exists"]) == 1:
        rand_id = random.randint(1, 10000)
        result = cursor.execute(exist_query)
    cursor.close()'''
    session["id"] = 0
    session["is_guest"] = "active"
    return redirect(url_for("movies.search_movie"))

@blp.route("/user/edit_info", methods=["GET", "POST"])
@login_required
def edit_info():
    form = EditUserForm()
    if form.validate_on_submit():
        user = User(int(session["id"]))
        fname = form.fname.data if form.fname.data != "" else None
        lname = form.lname.data if form.lname.data != "" else None
        email = form.email.data if form.email.data != "" else None
        username = form.username.data if form.username.data != "" else None
        pwrd = form.password.data if form.password.data != "" else None
        user.edit_info(fname, lname, email, username, pwrd)
        flash("User info was changed successfully.")
        #return redirect(url_for("user.login"))
    else:
        flash("user info was not updated.")
    return render_template("settings.html", form=form)

#logout of your account
@blp.route("/logout", methods=["GET"])
@login_required
def logout():
    session.pop("id")
    if "is_guest" in session:
        session.pop("is_guest")
    #flash("You were logged out successfully.", "success")
    if "id" not in session:
        return redirect(url_for("user.login", logout_msg="success"))
    return redirect(url_for("user.login"))

#returns home page of the logged in user
@blp.route("/home", methods=["GET"])
@login_required
def home_page():
    if "is_guest" in session:
        user = User(session["id"])
        user.username = "Guest" + str(session["id"])
    else:
        user = User(session["id"])
    return render_template("home_page.html", username=user.username)




@blp.route('/database')
def index():
    cur = mysql.connection.cursor()
    query = "CREATE TABLE  IF NOT EXISTS Person (id INT PRIMARY KEY, LastName VARCHAR(25))"
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return 'done'