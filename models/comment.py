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
        comments_query = "SELECT Comment.id as id, username, body, likes, dislikes, Comment.created FROM Comment, user WHERE forum_id={} AND user.id = Comment.owner".format(forum_id)
        comments = self.cursor.get_all_rows(comments_query)
        return comments

    def del_comment(self) -> None:
        pass

    def like_comment(self, comment_id:int, like_type:str) -> int:
        if like_type == "like":
            like_query = "UPDATE Comment SET Likes=Likes+1 WHERE id={}".format(comment_id)
            get_query = "SELECT Likes AS num FROM Comment WHERE id={}".format(comment_id)
        else:
            like_query = "UPDATE Comment SET dislikes=dislikes+1 WHERE id={}".format(comment_id)
            get_query = "SELECT dislikes AS num FROM Comment WHERE id={}".format(comment_id)
        self.cursor.update(like_query)
        return int(self.cursor.get_row(get_query)["num"])