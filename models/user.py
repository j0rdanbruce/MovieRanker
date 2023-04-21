from db import mysql
from flask_login import UserMixin
from  werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm

class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def get_user(self, email):
        cur = mysql.connection.cursor()
        query = "SELECT * FROM user WHERE email='{}'".format(email)
        cur.execute(query)
        mysql.connection.commit()
        user = cur.fetchone()
        cur.close()
        if user:
            return str(user)
    
    def insert_user(self, email, username, fname, lname, pwrd):
        cur = mysql.connection.cursor()
        query = "INSERT INTO user() VALUES()"
        cur.close()

    def get_id(self, email):
        cur = mysql.connection.cursor()
        query = "SELECT id FROM user WHERE email='{}'".format(email)
        cur.execute(query)
        mysql.connection.commit()
        user_id = cur.fetchone()
        cur.close()
        if user_id:
            return int(user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
