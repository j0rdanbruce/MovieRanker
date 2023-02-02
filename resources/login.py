from flask_smorest import Blueprint
from flask.views import MethodView
from flask import render_template

blp = Blueprint("login", __name__, description="operations for login")

@blp.route("/login")
class Login(MethodView):
    def get(self):
        return render_template("login.html")