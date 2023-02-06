from db import db

class FaveMovies(db.Model):
    __tablename__ = "favourite_movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    #director = db.Column(db.String(50), nullable=False)
    rank = db.Column(db.Integer, nullable=True)
    picture_url = db.Column(db.String, nullable=True)
    plot = db.Column(db.String, nullable=False, unique=False)
    movie_id = db.Column(db.Integer, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=False)

    user = db.relationship("UserModel", back_populates="fave_movies")