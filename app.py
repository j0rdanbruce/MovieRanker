import os

from flask import Flask
from flask import session
from flask_smorest import Api
from flask_login import LoginManager

from db import mysql
from models.user import User

#from flask_mysqldb import MySQL

from resources.movie import blp as MovieBlueprint
from resources.tv import blp as ShowBlueprint
from resources.actor import blp as ActorBlueprint
from resources.other import blp as OtherBlueprint
from resources.user import blp as UserBlueprint

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
app.config["SECRET_KEY"] = SECRET_KEY

#mysql = MySQL(app)
mysql.init_app(app)
api = Api(app)

'''with app.app_context():
    cur = mysql.connection.cursor()'''


api.register_blueprint(MovieBlueprint)
api.register_blueprint(ShowBlueprint)
api.register_blueprint(ActorBlueprint)
api.register_blueprint(OtherBlueprint)
api.register_blueprint(UserBlueprint)

#configuring a login manager for User Authintication purposes
login_manager = LoginManager()
login_manager.login_view = 'user.login_here'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)

'''@app.route('/database')
def index():
    cur = mysql.connection.cursor()
    query = "CREATE TABLE  IF NOT EXISTS Person (id INT PRIMARY KEY, LastName VARCHAR(25))"
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return 'done'
'''