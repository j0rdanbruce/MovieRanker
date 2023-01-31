from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

blp = Blueprint("actors", __name__, description="Operations for actors")