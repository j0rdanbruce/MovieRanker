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
from wrappers import login_required

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
def add_movies():
    if request.method == "POST":
        cursor = Cursor()
        movie_data = request.form.getlist("movie")
        lowest_rank = int(cursor.get_row("SELECT MAX(movie_rank) AS lowest_rank FROM Likes_Movie")["lowest_rank"])
        #open database connection
        cur = mysql.connection.cursor()
        query_1 = "INSERT INTO Movie(id, title, pic_url, plot) VALUES(%s, %s, %s, %s)"
        query_2 = "INSERT INTO Likes_Movie(user_id, movie_id, movie_rank) VALUES(%s, %s, %s)"
        for movie in movie_data:
            movie = json.loads(movie.replace('\'', '\"'))
            lowest_rank = lowest_rank + 1
            try:
                cur.execute(query_1, (int(movie['id']), movie['title'], movie['img_src'], movie['plot']))
            except MySQLdb.IntegrityError:
                pass
            cur.execute(query_2, (int(session["id"]), int(movie["id"]), lowest_rank))
        mysql.connection.commit()
        #close database connection
        cur.close()
        return redirect(url_for('user.home_page'))
    else:
        return {"message": "unsuccessful attempt"}

#TMDB Api calls here
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
        return render_template("movies.html", movies=movie_list)
    return render_template("search.html", form=form)

#application endpoint for users to view their liked movie list
@blp.route("/user/movie/movie_list", methods=["GET", "POST"])
@login_required
def get_liked_movies():
    cur = Cursor()
    if request.method == "GET":
        query = "select title, pic_url, plot, movie_rank, movie_id from Likes_Movie AS LM, Movie where LM.movie_id = Movie.id AND LM.user_id ={} order by movie_rank ASC".format(int(session["id"]))
        rank_query = "select movie_rank from Likes_Movie where user_id={} order by movie_rank asc".format(int(session["id"]))
        rank_list = []
        movie_data = cur.get_all_rows(query)
        for rank in cur.get_all_rows(rank_query):
            rank_list.append(rank["movie_rank"])
        return render_template("fave_movies.html", movies=movie_data, rank_list=rank_list)
    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        user = User(int(session["id"]))
        user.movie.remove_movie(movie_id)
        return redirect(url_for("movies.get_liked_movies"))

@blp.route("/user/movie/movie_list/movie_id:<string:movie_id>&current_rank:<string:current_rank>/change_rank", methods=["POST"])
def change_rank(movie_id, current_rank):
    new_rank = int(request.form.get("rank"))
    user = User(int(session["id"]))
    user.movie.changeRank(int(movie_id), int(current_rank), int(new_rank))
    return redirect(url_for("movies.get_liked_movies"))