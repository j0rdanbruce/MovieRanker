import os

from flask import Flask
from flask_smorest import Api
from flask import session
from flask_session import Session

from db import mysql

#from flask_mysqldb import MySQL

from resources.movie import blp as MovieBlueprint
from resources.tv import blp as ShowBlueprint
from resources.actor import blp as ActorBlueprint
from resources.other import blp as OtherBlueprint
from resources.user import blp as UserBlueprint
from resources.forum import blp as ForumBlueprint

from secret import SECRET_API_KEY, SECRET_KEY



app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "MovieRanker REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["MYSQL_HOST"] = 'sql.njit.edu'
app.config['MYSQL_USER'] = 'jeb79'
app.config['MYSQL_PASSWORD'] = 'Shumai123!'
app.config['MYSQL_DB'] = 'jeb79'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = SECRET_KEY

mysql.init_app(app)
api = Api(app)

'''with app.app_context():
    cur = mysql.connection.cursor()'''

#initializing session manager to flask app
Session(app)


api.register_blueprint(MovieBlueprint)
api.register_blueprint(ShowBlueprint)
api.register_blueprint(ActorBlueprint)
api.register_blueprint(OtherBlueprint)
api.register_blueprint(UserBlueprint)
api.register_blueprint(ForumBlueprint)
