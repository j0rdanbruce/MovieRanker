import uuid, json
from flask import request, render_template, redirect, url_for, session
from flask.views import MethodView
from flask_smorest import abort, Blueprint

import urllib.request, json, urllib.error
from secret import SECRET_API_KEY
#flask form for searching movies
from forms import SearchMovieForm
from db import movies, mysql, Cursor
from flask_mysqldb import MySQLdb
from models.user import User
from wrappers import login_required, sub_user_required
from forms import SearchMovieForm
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


#function endpoint for adding movies to my fave movie list
@blp.route("/picked_movies", methods=["POST"])
@login_required
def add_movies():
    if request.method == "POST":
        if "is_guest" in session:
            return "not subbed"
        user = User(int(session["id"]))
        movie_id = int(request.form.get("movie_id"))
        response = user.movie.add_movie(movie_id=movie_id)
        return response

#endpoint for searching movies
@blp.route("/search/movie", methods=["POST", "GET"])
def search_movie():
    form = SearchMovieForm()
    if form.validate_on_submit():
        movie_name = form.title.data
        movie_name = movie_name.replace(' ', '+')
        url = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(SECRET_API_KEY, movie_name)
        response = urllib.request.urlopen(url)
        movies_data = json.loads(response.read())
        base_movie_url = "https://image.tmdb.org/t/p/w400"
        movie_list = []
        for movie in movies_data["results"]:
            movie_data = {
                "id": movie["id"],
                "title": movie["original_title"],
                "plot": movie["overview"],
                "img_src": base_movie_url + str(movie["backdrop_path"])
            }
            movie_list.append(movie_data)
        return render_template("movies.html", form=form, movies=movie_list)
    message = request.args.get("login_message")
    if message:
        user = User(int(session["id"]))
        alert_msg = {}
        alert_msg["type"] = message
        alert_msg["message"] = "Hello, {}!".format(user.username)
        return render_template("movies.html", form=form, alert_message=alert_msg)
    return render_template("movies.html", form=form)

#application endpoint for users to view their liked movie list
@blp.route("/user/movie/movie_list", methods=["GET", "POST"])
@login_required
@sub_user_required
def get_liked_movies():
    cur = Cursor()
    if request.method == "GET":
        change_rank_alert_msg = request.args.get("message")
        query = "select title, pic_url, plot, movie_rank, movie_id from Likes_Movie AS LM, Movie where LM.movie_id = Movie.id AND LM.user_id ={} order by movie_rank ASC".format(int(session["id"]))
        rank_query = "select movie_rank from Likes_Movie where user_id={} order by movie_rank asc".format(int(session["id"]))
        rank_list = []
        movie_data = cur.get_all_rows(query)
        for rank in cur.get_all_rows(rank_query):
            rank_list.append(rank["movie_rank"])
        if "alert_message" in session:
            alert_msg = {}
            alert_msg["type"] = session["alert_message"]
            session.pop("alert_message")
            if alert_msg["type"] == "success":
                alert_msg["message"] = "Movie removed from your Fave Movie List"
        elif change_rank_alert_msg:
            alert_msg = {}
            alert_msg["type"] = change_rank_alert_msg
            alert_msg["message"] = "Movie Rank has been changed"
        else:
            return render_template("fave_movies.html", movies=movie_data, rank_list=rank_list)
        return render_template("fave_movies.html", movies=movie_data, rank_list=rank_list, alert_message=alert_msg)
    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        user = User(int(session["id"]))
        user.movie.remove_movie(movie_id)
        session["alert_message"] = "success"
        return redirect(url_for("movies.get_liked_movies"))

@blp.route("/user/movie/movie_list/movie_id:<string:movie_id>&current_rank:<string:current_rank>/change_rank", methods=["POST"])
def change_rank(movie_id, current_rank):
    new_rank = int(request.form.get("rank"))
    user = User(int(session["id"]))
    user.movie.changeRank(int(movie_id), int(current_rank), int(new_rank))
    return redirect(url_for("movies.get_liked_movies", message="success"))