from db import mysql, Cursor
from flask import flash, session, render_template
from  werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm

from models.forum import Forum
from models.comment import Comment
from models.movie import Movie

class User:
    '''Module that represents a user. Perform operations relative to users like registering new users to application and adding user to session.'''
    def __init__(self, id:int=None, email:str=None, pswrd:str=None, username:str=None) -> None:
        if id is not None and "is_guest" not in session:
            self.id = id
            self.get_user_by_id()
        else:
            self.id = id
        if email is not None:
            self.email = email
        if pswrd is not None:
            self.pswrd = pswrd
        if username is not None:
            self.username = username
        self.cursor = Cursor()
        self.forum = Forum()
        self.comment = Comment(id)
        self.movie = Movie()
    
    def get_user_by_id(self):
        cur = Cursor()
        query = "SELECT email, pwrd_hash, username FROM user WHERE id={}".format(self.id)
        result = cur.get_row(query) 
        self.email, self.pswrd, self.username = result["email"], result["pwrd_hash"], result["username"]

    def get_email(self) -> str:
        cur = Cursor()
        query = "SELECT email from user WHERE id={}".format(self.id)
        result = cur.get_row(query)
        if result:
            return result["email"]

    def get_pswrd(self) -> str:
        cur = Cursor()
        query = "SELECT pwrd_hash from user WHERE id={}".format(self.id)
        result = cur.get_row(query)
        if result:
            return result["pwrd_hash"]

    def get_username(self) -> str:
        cur = Cursor()
        query = "SELECT username from user WHERE id={}".format(self.id)
        result = cur.get_row(query)
        if result:
            return result["username"]
    
    def add_to_session(self) -> str:
        '''Adds the users unique integer \'id\' to the session.'''
        cur = mysql.connection.cursor()
        query = "SELECT * FROM user WHERE email='{}' AND pwrd_hash='{}'".format(self.email, self.pswrd)
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        if user:
            session["id"] = user["id"]
            return render_template("/home_page.html")
    
    def insert_user(self, fname: str, lname: str) -> None:
        '''Registers a new user's info to the database.'''
        cur = mysql.connection.cursor()
        query = "INSERT INTO user(fname, lname, email, username, pwrd_hash) VALUES(%s, %s, %s, %s, %s)"
        cur.execute(query, (fname, lname, self.email, self.username, self.pswrd))
        mysql.connection.commit()
        cur.close()

    def get_id(user_id: int) -> int:
        cur = mysql.connection.cursor()
        query = "SELECT * FROM user WHERE id='{}'".format(user_id)
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        if user:
            return User(user[4], user[5])

    def set_password(self, password) -> None:
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
        else:
            return False
    
    #user info related functions here
    def edit_info(self, fname:str=None, lname:str=None, email:str=None, username:str=None, pwrd:str=None):
        if fname is not None:
            query = "UPDATE user set fname='{}' where id={}".format(fname, self.id)
            self.cursor.update(query)
        if lname is not None:
            query = "UPDATE user set lname='{}' where id={}".format(lname, int(self.id))
            self.cursor.update(query)
        if email is not None:
            query = "UPDATE user set email='{}' where id={}".format(email, self.id)
            self.cursor.update(query)
        if username is not None:
            query = "UPDATE user set username='{}' where id={}".format(username, self.id)
            self.cursor.update(query)
        if pwrd is not None:
            query = "UPDATE user set pwrd_hash='{}' where id={}".format(pwrd, self.id)
            self.cursor.update(query)