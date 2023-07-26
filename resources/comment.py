from flask_smorest import Blueprint
from flask import session, render_template, redirect, url_for, request
from models.user import User
from forms import CommentForm
from wrappers import login_required

blp = Blueprint("comment", __name__, description="blueprint for comment related functions")

@blp.route("/forum/<forum_id>/comments", methods=["GET", "POST"])
@login_required
def comments(forum_id):
    form = CommentForm()
    user = User(id=int(session["id"]))
    if form.validate_on_submit():
        #make_comment()
        user.comment.make_comment(form.body.data, user.id, int(forum_id))
    forum_data = user.forum.get_forum(int(forum_id))
    comments = user.comment.get_comments(int(forum_id))
    for comment in comments:
        date = str(comment["created"]).split()[0]
        comment["created"] = date
    return render_template("comments.html", form=form, forum=forum_data, comments=comments)

@blp.route("/forum/comments/make_comment", methods=["POST"])
@login_required
def make_comment():
    return redirect(url_for("comment.comments"))