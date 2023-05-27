from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if "id" not in session or session["id"] is None:
            flash("Must be logged in to view this page.", "message")
            return redirect(url_for("user.login"))
        return func(*args, **kwargs)
    return decorated_func