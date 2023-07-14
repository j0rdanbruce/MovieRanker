from functools import wraps
from flask import session, flash, redirect, url_for

#allows valid scubscribers or guest subscirbers access
def login_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if "id" not in session or session["id"] is None:
            flash("Must be logged in to view this page.", "message")
            return redirect(url_for("user.login"))
        return func(*args, **kwargs)
    return decorated_func

#wrapper only allows subscribed users witht he aplication to view the page
def sub_user_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if "is_guest" in session:
            flash("Must be a valid subscriber to view this page.", "message")
            return redirect(url_for("user.login"))
        return func(*args, **kwargs)
    return decorated_func