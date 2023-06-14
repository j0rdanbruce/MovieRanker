from db import Cursor
from flask import session


class Movie():
    '''Module that represents a movie and performs functions for movie content.'''
    def __init__(self) -> None:
        self.cursor = Cursor()

    def changeRank(self, movie_id: int, current_rank: int, new_rank: int):
        id_query = "select movie_id from Likes_Movie where user_id={} and movie_rank >={} and movie_rank < {} order by movie_rank asc".format(int(session["id"]), new_rank, current_rank)
        rank_query = "update Likes_Movie set movie_rank = {} where movie_id={} and user_id={}".format(new_rank, movie_id, int(session["id"]))
        movies = self.cursor.get_all_rows(id_query)
        self.cursor.update(rank_query)
        for movie in movies:
            movie_id = int(movie["movie_id"])
            update_query = "update Likes_Movie set movie_rank = movie_rank + 1 where movie_id={}".format(movie_id)
            self.cursor.update(update_query)