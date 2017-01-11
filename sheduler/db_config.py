from model.orm_models import *


class DBConfig:
    def __init__(self):
        create_tables()

    def create_users(self, users):
        for user in users:
            User.create(id=user.id, first_name=user.first_name, last_name=user.last_name,
                    photo=user.photo, is_member=user.is_member)

    def get_users(self):
        return User.select()

    def get_members(self):
        return User.select().where(User.is_member)

    def get_not_members(self):
        return User.select().where(~User.is_member)

    def update_user(self, user):
        db_user = User.get(User.id == user.id)
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.photo = user.photo
        db_user.is_member = user.is_member
        db_user.save()

    def delete_users(self, users_ids):
        for user_id in users_ids:
            user = User.get(User.id == user_id)
            q = Friend.delete().where(Friend.user == user)
            q1 = Friend.delete().where(Friend.friend == user)
            q2 = Post.delete().where(Post.user == user)
            q.execute()
            q1.execute()
            q2.execute()
            user.delete_instance()


    def get_friends(self, user_id):
        db_user = User.get(User.id == user_id)
        return User.select(User).join(Friend, on=Friend.friend).where(Friend.user == db_user)

    def delete_friends(self, user_id, friends_ids):
        db_user = User.get(User.id == user_id)
        for friend_id in friends_ids:
            db_friend = User.get(User.id == friend_id)
            Friend.get((Friend.user == db_user) & (Friend.friend == db_friend)).delete_instance()

    def create_friend(self, user_id, friend_id):
        db_user = User.get(User.id == user_id)
        db_friend = User.get(User.id == friend_id)
        Friend.create(user=db_user, friend=db_friend)

    def get_posts(self, user_id):
        db_user = User.get(User.id == user_id)
        return Post.select().where(Post.user == db_user)

    def create_post(self, post):
        db_user = User.get(User.id == post.user_id)
        Post.create(user=db_user, post_id=post.post_id, text=post.text, date=post.date,
                    comments_count=post.comments_count, likes_count=post.likes_count, reposts_count=post.reposts_count,
                    normalized_comments=post.normalized_comments, normalized_likes=post.normalized_likes,
                    normalized_reposts=post.normalized_reposts, share_count=post.share_count,
                    reposted_from=post.reposted_from, attachments=post.attachments)

    def update_post(self, post):
        db_user = User.get(User.id == post.user_id)
        db_post = Post.get((Post.user == db_user) & (Post.post_id == post.post_id))
        db_post.text = post.text
        db_post.date = post.date
        db_post.comments_count = post.comments_count
        db_post.likes_count = post.likes_count
        db_post.reposts_count = post.reposts_count
        db_post.normalized_comments = post.normalized_comments
        db_post.normalized_likes = post.normalized_likes
        db_post.normalized_reposts = post.normalized_reposts
        db_post.share_count = post.share_count
        db_post.reposted_from = post.reposted_from
        db_post.attachments = post.attachments
        db_post.save()

    def delete_posts(self, posts_ids):
        for post_id in posts_ids:
            user_id, db_post_id = post_id.split('_')
            db_user = User.get(User.id == user_id)
            Post.get((Post.user == db_user) & (Post.post_id == db_post_id)).delete_instance()