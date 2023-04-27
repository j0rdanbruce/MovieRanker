from db import mysql
from flask_login import UserMixin
from flask import flash
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
        user = cur.fetchone()
        cur.close()
        if user:
            id = user[0]
            return str(user)
    
    def insert_user(self, fname, lname, email, username):
        cur = mysql.connection.cursor()
        query = "INSERT INTO user(fname, lname, email, username, pwrd_hash) VALUES(%s, %s, %s, %s, %s)"
        cur.execute(query, (fname, lname, email, username, self.password_hash))
        mysql.connection.commit()
        cur.close()

    def get_id(user_id):
        cur = mysql.connection.cursor()
        query = "SELECT id FROM user WHERE id='{}'".format(user_id)
        cur.execute(query)
        user_id = cur.fetchone()
        cur.close()
        if user_id:
            return str(user_id)

    def set_password(self, password):
        form = RegistrationForm()
        if form.password1.data == form.password2.data:
            self.password_hash = generate_password_hash(password)
        else:
            flash('Password does not match', 'error')
    
    def check_password(self, password):
        cur = mysql.connection.cursor()
        query = "SELECT pwrd_hash FROM user WHERE email='{}'".format(self.email)
        cur.execute(query)
        pwrd_hash = cur.fetchone()
        cur.close()
        return True
