import requests
import requests.exceptions


class VKRequests:
    def get_members(self, group_id):
        resp = requests.get("https://api.vk.com/method/groups.getMembers", timeout=100,
                        params={"group_id": group_id, "fields": "photo_100", "v": 5.57})
        members = resp.json()['response']['items']
        return members

    def get_friends(self, user_id):
        resp = requests.get('https://api.vk.com/method/friends.get', timeout=100,
                        params={"user_id": user_id, "fields": "photo_100", "v": 5.57})
        if 'response' in resp.json():
            friends = resp.json()['response']['items']
        else:
            friends = []
            print(resp.json())
        return friends

    def get_posts(self, user_id, offset):
        resp = requests.get('https://api.vk.com/method/wall.get', timeout=100,
                        params={"owner_id": user_id, "fields": {"n"},
                                "v": 5.57, "filter": "owner", "offset": offset, "count": 100})
        if 'response' in resp.json():
            posts = resp.json()['response']['items']
        else:
            posts = []
            print(resp.json())
        return posts
