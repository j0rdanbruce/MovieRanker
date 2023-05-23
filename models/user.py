from db import mysql
from flask import flash, session, render_template
from  werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm

class User:
    def __init__(self, username=None, email=None, pswrd=None):
        self.email = email
        self.pswrd = pswrd
        self.username = username
    
    def add_to_session(self):
        cur = mysql.connection.cursor()
        query = "SELECT * FROM user WHERE email='{}' AND pwrd_hash='{}'".format(self.email, self.pswrd)
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        if user:
            session["id"] = user["id"]
            return render_template("/home_page.html")
    
    def insert_user(self, fname, lname):
        cur = mysql.connection.cursor()
        query = "INSERT INTO user(fname, lname, email, username, pwrd_hash) VALUES(%s, %s, %s, %s, %s)"
        cur.execute(query, (fname, lname, self.email, self.username, self.pswrd))
        mysql.connection.commit()
        cur.close()

    def get_id(user_id):
        cur = mysql.connection.cursor()
        query = "SELECT * FROM user WHERE id='{}'".format(user_id)
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        if user:
            return User(user[4], user[5])

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
    
    def is_authenticated(self):
        if session["id"] is not None:
            return True
