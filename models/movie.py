from db import db

class FaveMovies(db.Model):
    __tablename__ = "favourite_movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    #director = db.Column(db.String(50), nullable=False)
    rank = db.Column(db.Integer, nullable=True)
    picture_url = db.Column(db.String, nullable=True)
    movie_id = db.Column(db.Integer, nullable=False, unique=True)