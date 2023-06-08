from db import Cursor

class Forum():
    '''A model that represents a forum. users can make, delete, comment, etc. on forums within this application.
    This class allows implementation of CRUD features for forums.'''
    def __init__(self) -> None:
        self.cursor = Cursor()

    def create_forum(self, title: str, body: str, user_id: int, private: bool) -> None:
        query = "INSERT INTO Forum(title, body, owner, private) VALUES(%s, %s, %s, %s)"
        values = (title, body, user_id, private)
        self.cursor.insert(query, values)
    
    def get_my_forums(self):
        pass

    def get_all_forums(self) -> list[dict]:
        query = "select id, title, body, upvote - downvote as votes from Forum LIMIT 50"
        result = self.cursor.get_all_rows(query)
        if result:
            return result
    
    def upVote(self, forum_id:int) -> int:
        update_query = "UPDATE Forum SET upvote = upvote + 1 WHERE id={}".format(forum_id)
        sel_query = "SELECT upvote - downvote as votes FROM Forum WHERE id={}".format(forum_id)
        self.cursor.update(update_query)
        result = self.cursor.get_row(sel_query)
        if result:
            return int(result["votes"])