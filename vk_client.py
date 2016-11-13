from vk_requests import *
from models.vk_models import *

class VK_client:

    def __init__(self):
        self.vk_requests = VK_requests()


    def get_members(self):
        return [User(member['id'], member['first_name'], member['last_name'],
                     member['photo_100'] if 'photo_100' in member else None, True)
                for member in self.vk_requests.get_members()
                if 'deactivated' not in member]

    def get_friends(self, user_id):
        return {"user_id": user_id, "friends": [User(friend['id'], friend['first_name'], friend['last_name'],
                     friend['photo_100'] if 'photo_100' in friend else None, False)
                for friend in self.vk_requests.get_friends(user_id)
                if 'deactivated' not in friend and 'hidden' not in friend]}