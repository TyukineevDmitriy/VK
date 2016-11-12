from vk_client import *
from config.db_config import *

class DB_updater:

    def __init__(self):
        self.vk_client = VK_client()
        self.db = DB_config()

    def update(self):
        unique_users_ids = []
        db_users_ids = set([user.id for user in self.db.get_users()])
        vk_users = self.vk_client.get_members()
        for user in vk_users:
            if user.id in db_users_ids:
                self.db.update_user(user)
            else:
                self.db.create_users([user])
            unique_users_ids.append(user.id)
        friends_of_members = []
        pool = ThreadPool(50)
        friends_of_members.extend(pool.map(self.vk_client.get_friends, [user.id for user in vk_users]))
        pool.close()
        pool.join()
        for member in friends_of_members:
            db_friends = self.db.get_friends_of_user(member['user_id'])
            db_friends_ids = [friend.id for friend in db_friends] if db_friends is not None else []
            for friend in member['friends']:
                if friend.id not in unique_users_ids:
                    if friend.id in db_users_ids:
                        self.db.update_user(friend)
                    else:
                        self.db.create_users([friend])
                    unique_users_ids.append(friend.id)
                if friend.id not in db_friends_ids:
                    self.db.create_friend(member['user_id'], friend.id)
            db_friends_ids = set(db_friends_ids if db_friends is not None else [])
            self.db.delete_friends(member['user_id'], db_friends_ids.difference(
                [friend.id for friend in member['friends']]))
        self.db.delete_users(db_users_ids.difference(unique_users_ids))
