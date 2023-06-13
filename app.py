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
from resources.comment import blp as CommentBlueprint

from secret import SECRET_API_KEY, SECRET_KEY


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "MovieRanker REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["MYSQL_HOST"] = "83.229.67.41" or os.getenv("mysql_host")
    app.config['MYSQL_USER'] = "root" or os.getenv("mysql_user")
    app.config['MYSQL_PASSWORD'] = "M@nkeyBus!ne$$96!" or os.getenv("mysql_pwrd")
    app.config["MYSQL_DB"] = "MovieRanker" or os.getenv("mysql_db_name")
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
    api.register_blueprint(CommentBlueprint)

    return app