#from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

#db = SQLAlchemy()
mysql = MySQL()

movies = {}
shows = {}
actors = {}

class Cursor:
    '''Cursor module for connecting to database and performing basic CRUD operations with MySQL.'''
    def insert_query(self, query: str, values: tuple):
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, values)
        except:
            return {"message": "Unsuccessful insert query."}
        mysql.connection.commit()
        cur.close()
    
    def multiple_insert_query(self, query: str, data_list: list):
        cur = mysql.connection.cursor()
        for data in data_list:
            values = ()
            for value in data:
                pass
            cur.execute(query, values)
        mysql.connection.commit()
        cur.close()
    
    def delete(self, query: str):
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
        except:
            pass
        mysql.connection.commit()
        cur.close()

    def update(self, query: str):
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
        except:
            pass
        mysql.connection.commit()
        cur.close()