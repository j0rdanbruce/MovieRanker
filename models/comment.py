from db import Cursor

class Comment():
    def __init__(self, user_id:int=None) -> None:
        self.user_id = user_id
        self.cursor = Cursor()

    def make_comment(self, body:str, owner_id:int, forum_id:int) -> None:
        '''Function for making comments on a Forum post'''
        query = "INSERT INTO Comment(body, owner, forum_id) VALUES(%s, %s, %s)"
        values = (body, owner_id, forum_id)
        self.cursor.insert(query, values)
    
    def get_comments(self, forum_id: int) -> list[dict]:
        '''return a list of dictionaries containing the comment and username of commenter.'''
        comments_query = "SELECT username, body, Comment.created FROM Comment, user WHERE forum_id={} AND user.id = Comment.owner".format(forum_id)
        comments = self.cursor.get_all_rows(comments_query)
        return comments

    def del_comment(self) -> None:
        pass

    def like_comment(self, comment_id:int) -> None:
        pass