import requests
from math import ceil


# mhi = 91925201
# iit = 30390813

class VK_requests:
    def get_members(self):
        resp = requests.get("https://api.vk.com/method/groups.getMembers",
                            params={"group_id": 91925201, "fields": "photo_100", "v": 5.57})
        members = resp.json()['response']['items']
        return members

    def get_friends(self, user_id):
        resp = requests.get('https://api.vk.com/method/friends.get',
                            params={"user_id": user_id, "fields": "photo_100", "v": 5.57})
        friends = resp.json()['response']['items']
        for friend in friends:
            if 'deactivated' in friend or 'hidden' in friend:
                friends.remove(friend)
        return friends

    def __get_user_posts(self, user_id, offset):
        resp = requests.get('https://api.vk.com/method/wall.get',
                            params={"owner_id": user_id, "fields": {"n"},
                                    "v": 5.57, "filter": "owner", "offset": offset, "count": 100})
        return resp.json()['response']['items']

    def get_all_user_posts(self, user_id):
        user_posts = []
        count = requests.get('https://api.vk.com/method/wall.get',
                             params={"owner_id": user_id, "filter": "owner", "fields": {"n"}, "v": 5.57})
        count = ceil(count.json()['response']['count'] / 100)
        for i in range(ceil(count)):
            task = self.__get_user_posts(user_id, i * 100)
            user_posts.extend(task)
        return user_posts
