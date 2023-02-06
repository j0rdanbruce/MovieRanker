from db import db
from flask_login import UserMixin
from datetime import datetime

from  werkzeug.security import generate_password_hash, check_password_hash

class UserModel(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False)
    email = db.Column(db.String(150), index=True, nullable=False)
    password_hash = db.Column(db.String(150), unique=True, nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    modified = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    fave_movies = db.relationship("FaveMovies", back_populates="user", lazy="dynamic", cascade="all, delete")
