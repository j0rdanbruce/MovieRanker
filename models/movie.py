from db import Cursor
from flask import session
from models.tmdb_api import TMDB_API
from flask_mysqldb import MySQLdb

class Movie():
    '''Module that represents a movie and performs functions for movie content.'''
    def __init__(self) -> None:
        self.cursor = Cursor()
        self.tmdb_api = TMDB_API()

    def changeRank(self, movie_id: int, current_rank: int, new_rank: int):
        rank_query = "update Likes_Movie set movie_rank = {} where movie_id={} and user_id={}".format(new_rank, movie_id, int(session["id"]))
        if current_rank > new_rank:
            id_query = "select movie_id from Likes_Movie where user_id={} and movie_rank >={} and movie_rank < {} order by movie_rank asc".format(int(session["id"]), new_rank, current_rank)
            movies = self.cursor.get_all_rows(id_query)
            self.cursor.update(rank_query)
            for movie in movies:
                movie_id = int(movie["movie_id"])
                update_query = "update Likes_Movie set movie_rank = movie_rank + 1 where movie_id={}".format(movie_id)
                self.cursor.update(update_query)
        elif current_rank < new_rank:
            id_query = "select movie_id from Likes_Movie where user_id={} and movie_rank > {} and movie_rank <= {} order by movie_rank asc".format(int(session["id"]), current_rank, new_rank)
            movies = self.cursor.get_all_rows(id_query)
            self.cursor.update(rank_query)
            for movie in movies:
                movie_id = int(movie["movie_id"])
                update_query = "update Likes_Movie set movie_rank = movie_rank - 1 where movie_id={}".format(movie_id)
                self.cursor.update(update_query)
        else:
            pass
    
    def add_movie(self, movie_id: int) -> None:
        movie_data = self.tmdb_api.get_movie_data(movie_id)
        image_url = "https://image.tmdb.org/t/p/w400" + movie_data["backdrop_path"]
        query_1 = "INSERT INTO Movie(id, title, pic_url, plot) VALUES(%s, %s, %s, %s)"
        query_2 = "INSERT INTO Likes_Movie(user_id, movie_id, movie_rank) VALUES(%s, %s, %s)"
        lowest_rank = int(self.cursor.get_row("SELECT MAX(movie_rank) AS lowest_rank FROM Likes_Movie WHERE user_id={}".format(int(session["id"])))["lowest_rank"])
        lowest_rank = lowest_rank + 1
        try:
            self.cursor.insert(query_1, (int(movie_data["id"]), movie_data["title"], image_url, movie_data["overview"]))
        except MySQLdb.IntegrityError:
            pass
        try:
            self.cursor.insert(query_2, (int(session["id"]), int(movie_data["id"]), lowest_rank))
        except MySQLdb.IntegrityError:
            pass

    def remove_movie(self, movie_id: int) -> None:
        movie_rank = int(self.cursor.get_row("SELECT movie_rank FROM Likes_Movie WHERE user_id={} AND movie_id={}".format(int(session["id"]), int(movie_id)))["movie_rank"])
        del_query = "DELETE FROM Likes_Movie WHERE user_id={} AND movie_id={}".format(int(session["id"]), movie_id)
        movies = self.cursor.get_all_rows("SELECT movie_id, movie_rank FROM Likes_Movie WHERE movie_rank > {} AND user_id={}".format(movie_rank, int(session["id"])))
        self.cursor.delete(del_query)
        for movie in movies:
            update_query = "UPDATE Likes_Movie SET movie_rank={} WHERE movie_id={} AND user_id={}".format((int(movie["movie_rank"])-1), int(movie["movie_id"]), int(session["id"]))
            self.cursor.update(update_query)