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
    
    def get_forum(self, forum_id: int):
        query = "SELECT Forum.id, title, body, upvote - downvote as votes, username FROM Forum, user WHERE user.id = owner AND Forum.id={}".format(forum_id)
        result = self.cursor.get_row(query)
        if result:
            return result

    def get_all_forums(self) -> list[dict]:
        query = "select Forum.id, Forum.title, Forum.body, upvote - downvote as votes, coalesce(count(Comment.body), 0) as no_comments from Forum left join Comment on Forum.id=Comment.forum_id group by id order by votes DESC LIMIT 50"
        result = self.cursor.get_all_rows(query)
        if result:
            return result
    
    def upVote(self, vote_type:str, forum_id:int) -> int:
        if vote_type == "upvote":
            update_query = "UPDATE Forum SET upvote = upvote + 1 WHERE id={}".format(forum_id)
        else:
            update_query = "UPDATE Forum SET downvote = downvote + 1 WHERE id ={}".format(forum_id)
        sel_query = "SELECT upvote - downvote as votes FROM Forum WHERE id={}".format(forum_id)
        self.cursor.update(update_query)
        result = self.cursor.get_row(sel_query)
        if result:
            return int(result["votes"])
