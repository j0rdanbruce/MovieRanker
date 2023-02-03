import uuid, json
from flask import request, render_template
from flask.views import MethodView
from flask_smorest import abort, Blueprint

import urllib.request, json, urllib.error
from secret import SECRET_API_KEY

from db import movies

from schemas import PlainMovieSchema

blp = Blueprint("movies", __name__, description="Operations for movies")

@blp.route("/movie")
class MovieList(MethodView):
    @blp.response(200, PlainMovieSchema(many=True))
    def get(self):
        return list(movies.values())
    
    @blp.arguments(PlainMovieSchema)
    @blp.response(201, PlainMovieSchema)
    def post(self, movie_data):
        movie_id = uuid.uuid4().hex
        movie_data = {**movie_data, "id": movie_id}
        movies[movie_id] = movie_data
        return movie_data


@blp.route("/movie/<string:movie_id>")
class Movie(MethodView):
    @blp.response(200, PlainMovieSchema)
    def get(self, movie_id):
        try:
            return movies[movie_id]
        except KeyError:
            abort(404, message="Movie not found in database.")

    def delete(self, movie_id):
        pass

    def put(self, movie_id):
        pass

#reutrn string dictionary of picked movies. this is not optimal. sending dictionary from html in string form. fix later.
@blp.route("/picked_movies", methods=["POST"])
def get_picked_movies():
    if request.method == "POST":
        movie_data = request.form.getlist("movie")
        for movie in movie_data:
            movie = json.loads(movie.replace('\'', '\"'))
            return movie
        #return movie_data
    else:
        return {"message": "unsuccessful attempt"}
    

#TMDB Api calls here
@blp.route("/movies/<string:movie_name>")
class TMDB_Calls(MethodView):
    #@blp.response(200, PlainMovieSchema(many=True))
    def get(self, movie_name):
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