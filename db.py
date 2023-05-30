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
    
    def multiple_insert_query(self, cursor, query: str):
        cursor.execute(query)
        cursor.close()
    
    def get_all_rows(self, query: str) -> list:
        '''returns a list of all tuples from the query paramter in dictionary format.'''
        return_results = []
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        for tuple in results:
            return_results.append(tuple)
        return return_results

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