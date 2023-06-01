from db import Cursor

class Forum():
    '''A model that represents a forum. users can make, delete, comment, etc. on forums within this application.
    This class allows implementation of CRUD features for forums.'''
    def __init__(self) -> None:
        self.cursor = Cursor()

    def create_forum(self, title: str, body: str, user_id: int) -> None:
        query = "INSERT INTO Forum(title, body, owner) VALUES(%s, %s, %s)"
        values = (title, body, user_id)
        self.cursor.insert(query, values)
    
    def get_my_forums(self):
        pass

    def get_all_forums(self):
        pass

