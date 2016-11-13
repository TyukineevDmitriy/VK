from models.orm_models import *


class DB_config:
    def __init__(self):
        create_tables()

    def create_users(self, users):
        for user in users:
            User.create(id=user.id, first_name=user.first_name, last_name=user.last_name,
                    photo=user.photo, is_member=user.is_member)

    def get_users(self):
        return User.select()

    def update_user(self, user):
        db_user = User.get(User.id == user.id)
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.photo = user.photo
        db_user.is_member = user.is_member
        db_user.save()

    def delete_users(self, users_ids):
        for user_id in users_ids:
            print(user_id)
            User.get(User.id == user_id).delete_instance()

    def get_friends_of_user(self, user_id):
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