from flask import request, render_template
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from jinja2 import TemplateNotFound

blp = Blueprint("other", __name__, description="miscellaneous operations")

@blp.route("/")
def showIndex():
    try:
        return render_template("layout.html")
    except TemplateNotFound:
        abort(404, message="Template was not found.")
