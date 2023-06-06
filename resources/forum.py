from flask_smorest import Blueprint
from flask import session, render_template, redirect, url_for
from forms import ForumForm

from models.user import User

from wrappers import login_required

blp = Blueprint("forum", __name__, description="blueprint for forum related functions")

@blp.route("/forum/get_forums", methods=["GET"])
def get_forums():
    user = User(id=int(session["id"]))
    forums = user.forum.get_all_forums()
    return render_template("see_forums.html", forums=forums)

@blp.route("/forum/my_forums", methods=["GET"])
def my_forums():
    user = User(id=int(session["id"]))

    return render_template("my_forums.html")

@blp.route("/forum/create_forum", methods=["GET", "POST"])
@login_required
def create_forum():
    form = ForumForm()
    if form.validate_on_submit():
        user = User(id=int(session["id"]))
        user.forum.create_forum(form.title.data, form.body.data, user.id, form.private.data)
        return redirect(url_for("forum.my_forums"))
    return render_template("my_forums.html", form=form)

