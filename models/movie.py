from db import Cursor
from flask import session


class Movie():
    '''Module that represents a movie and performs functions for movie content.'''
    def __init__(self) -> None:
        self.cursor = Cursor()

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
    
    def add_movie(self, ) -> None:
        pass

    def remove_movie(self, movie_id: int) -> None:
        movie_rank = int(self.cursor.get_row("SELECT movie_rank FROM Likes_Movie WHERE user_id={} AND movie_id={}".format(int(session["id"]), int(movie_id)))["movie_rank"])
        del_query = "DELETE FROM Likes_Movie WHERE user_id={} AND movie_id={}".format(int(session["id"]), movie_id)
        movies = self.cursor.get_all_rows("SELECT movie_id, movie_rank FROM Likes_Movie WHERE movie_rank > {} AND user_id={}".format(movie_rank, int(session["id"])))
        self.cursor.delete(del_query)
        for movie in movies:
            update_query = "UPDATE Likes_Movie SET movie_rank={} WHERE movie_id={} AND user_id={}".format((int(movie["movie_rank"])-1), int(movie["movie_id"]), int(session["id"]))
            self.cursor.update(update_query)