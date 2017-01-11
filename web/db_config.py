from model.orm_models import *

class DBConfig:
    def __init__(self):
        self.__sortings = ['by_date', 'by_comments', 'by_likes', 'by_reposts', 'by_normalized_comments',
                  'by_normalized_likes', 'by_normalized_reposts', 'by_shares']

    def get_sorted_news_feed(self, user, sorting):
        if sorting not in self.__sortings:
            return []
        if sorting == 'by_date':
            sort_by = 'date'
        elif sorting == 'by_comments':
            sort_by = 'comments_count'
        elif sorting == 'by_likes':
            sort_by = 'likes_count'
        elif sorting == 'by_reposts':
            sort_by = 'reposts_count'
        elif sorting == 'by_normalized_comments':
            sort_by = 'normalized_comments'
        elif sorting == 'by_normalized_likes':
            sort_by = 'normalized_likes'
        elif sorting == 'by_normalized_reposts':
            sort_by = 'normalized_reposts'
        else:
            sort_by = 'share_count'
        s = "Post.select(Post, User, Friend).join(User, JOIN.LEFT_OUTER).join(Friend, JOIN.LEFT_OUTER, Friend.friend)\
            .where(Friend.user == user).order_by(Post.{}.desc())".format(sort_by)
        query = eval(s)
        return query

    def get_user(self, user_id):
        return User.get(User.id == user_id)

    def get_members(self):
        return User.select().where(User.is_member)