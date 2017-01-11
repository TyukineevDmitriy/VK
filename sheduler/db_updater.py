from multiprocessing.dummy import Pool as ThreadPool

from api.fb_requests import FBRequests
from client.vk_client import VKClient
from sheduler.db_config import DBConfig

class DBUpdater:

    def __init__(self):
        self.__vk_client = VKClient(FBRequests.get_share_count)
        self.__db = DBConfig()

    def update_db(self):
        self.__update_users()
        self.__update_posts()

    def __update_users(self):
        unique_users_ids = []
        db_users_ids = set([user.id for user in self.__db.get_users()])
        vk_users = self.__vk_client.get_members()
        for user in vk_users:
            if user.id in db_users_ids:
                self.__db.update_user(user)
            else:
                self.__db.create_users([user])
            unique_users_ids.append(user.id)
        with ThreadPool(30) as pool:
            friends_of_members = pool.map(self.__vk_client.get_friends, [user.id for user in vk_users])
        for member in friends_of_members:
            db_friends = self.__db.get_friends(member['user_id'])
            db_friends_ids = [friend.id for friend in db_friends] if db_friends is not None else []
            for friend in member['friends']:
                if friend.id not in unique_users_ids:
                    if friend.id in db_users_ids:
                        self.__db.update_user(friend)
                    else:
                        self.__db.create_users([friend])
                    unique_users_ids.append(friend.id)
                if friend.id not in db_friends_ids:
                    self.__db.create_friend(member['user_id'], friend.id)
            db_friends_ids = set(db_friends_ids)
            self.__db.delete_friends(member['user_id'], db_friends_ids.difference(
                [friend.id for friend in member['friends']]))
        self.__db.delete_users(db_users_ids.difference(unique_users_ids))

    def __update_posts(self):
        db_not_member_users_ids = [user.id for user in self.__db.get_not_members()]
        with ThreadPool(30) as pool:
            pool.map(self.__update_users_posts, db_not_member_users_ids)

    def __update_users_posts(self, user_id):
        db_posts = self.__db.get_posts(user_id)
        db_posts_ids = ["{}_{}".format(p.user.id, p.post_id) for p in db_posts]
        vk_posts = self.__vk_client.get_posts(user_id)
        for vk_post in vk_posts:
            if "{}_{}".format(vk_post.user_id, vk_post.post_id) not in db_posts_ids:
                self.__db.create_post(vk_post)
            else:
                self.__db.update_post(vk_post)
        vk_posts_ids = set(["{}_{}".format(p.user_id, p.post_id) for p in vk_posts])
        db_posts_ids = set(db_posts_ids)
        self.__db.delete_posts(db_posts_ids.difference(vk_posts_ids))

