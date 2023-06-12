from db import Cursor

class Comment():
    def __init__(self, user_id:int=None) -> None:
        self.user_id = user_id

    def make_comment(self, body:str, owner_id:int, forum_id:int) -> None:
        '''Function for making comments on a Forum post'''
        cur = Cursor()
        query = "INSERT INTO Comment(body, owner, forum_id) VALUES(%s, %s, %s)"
        values = (body, owner_id, forum_id)
        cur.insert(query, values)

    def del_comment(self) -> None:
        pass

    def like_comment(self, comment_id:int) -> None:
        pass