import os

from flask import Flask, render_template, request
from flask_smorest import Api
from flask_login import LoginManager

from db import db
import models

from resources.movie import blp as MovieBlueprint
from resources.tv import blp as ShowBlueprint
from resources.actor import blp as ActorBlueprint
from resources.other import blp as OtherBlueprint
from resources.user import blp as UserBlueprint

from secret import SECRET_API_KEY, SECRET_KEY

def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY

    db.init_app(app)
    api = Api(app)
    
    with app.app_context():
        db.create_all()

    api.register_blueprint(MovieBlueprint)
    api.register_blueprint(ShowBlueprint)
    api.register_blueprint(ActorBlueprint)
    api.register_blueprint(OtherBlueprint)
    api.register_blueprint(UserBlueprint)

    #configuring a login manager for User Authintication purposes
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.get(user_id)

    return app

'''@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/search")
def search_page():
    return render_template("searchMovies.html")

@app.get("/movies/<string:movie_name>")
def get_movies_list_by_title(movie_name):
    #figure out environment paths later
    url = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(SECRET_API_KEY, movie_name)
    response = urllib.request.urlopen(url)
    movies_data = json.loads(response.read())
    base_movie_url = "https://image.tmdb.org/t/p/w400"
    movie_list = []
    for movie in movies_data["results"]:
        movie_id = movie["id"]
        movie_data = {
            "title": movie["original_title"],
            "plot": movie["overview"],
            "id": movie_id,
            "img_src": base_movie_url + str(movie["backdrop_path"])
        }
        movie_list.append(movie_data)
    #return movie_list, 201
    return render_template("movies.html", movies=movie_list)

@app.get("/actors/<string:actor_name>")
def get_actors_by_name(actor_name):
    url = "https://api.themoviedb.org/3/search/person?api_key={}&query={}".format(SECRET_API_KEY, actor_name)
    response = urllib.request.urlopen(url)
    actors_data = json.loads(response.read())
    base_actor_url = "https://image.tmdb.org/t/p/w400"
    actor_list = []
    for actor in actors_data["results"]:
        actor_data = {
            "actor_id": actor["id"],
            "actor_name": actor["name"],
            "img_src": base_actor_url + str(actor["profile_path"]),
            "popularity": actor["popularity"]
        }
        actor_list.append(actor_data)
    #return actor_list, 200
    return render_template("actors.html", actors=actor_list)'''