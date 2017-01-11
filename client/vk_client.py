from datetime import datetime, timedelta

from api.vk_requests import *
from model.vk_models import *


class VKClient:
    def __init__(self, get_share_count):
        self.__vk_requests = VKRequests()
        self.__get_share_count = get_share_count
        self.__group_id = 30390813

    def get_members(self):
        return [User(member['id'], member['first_name'], member['last_name'],
                     member['photo_100'] if 'photo_100' in member else None, True)
                for member in self.__vk_requests.get_members(self.__group_id)
                if 'deactivated' not in member]

    def get_friends(self, user_id):
        return {"user_id": user_id, "friends": [User(friend['id'], friend['first_name'], friend['last_name'],
                                                     friend['photo_100'] if 'photo_100' in friend else None, False)
                                                for friend in self.__vk_requests.get_friends(user_id)
                                                if 'deactivated' not in friend and 'hidden' not in friend]}

    def get_posts(self, user_id):
        posts = []
        offset = 0
        posts_are_in_time_interval = True
        while posts_are_in_time_interval:
            user_posts = self.__vk_requests.get_posts(user_id, offset)
            user_friends_count = len(self.__vk_requests.get_friends(user_id))
            for post in user_posts:
                post_date = datetime.fromtimestamp(post['date'])
                if post_date < (datetime.now() - timedelta(days=1)):
                    posts_are_in_time_interval = False
                    break
                attachments = None
                share_count = None
                if 'attachments' in post:
                    attachments, share_count = self.__parse_attachments(post['attachments'])
                reposted_from = None
                if 'copy_history' in post:
                    copy_history = post['copy_history'][0]
                    reposted_from = "{}_{}".format(copy_history['owner_id'], copy_history['id'])
                posts.append(Post(post['owner_id'], post['id'], post['text'], post_date
                                  , post['comments']['count'], post['likes']['count'], post['reposts']['count'],
                                  post['comments']['count'] / user_friends_count if user_friends_count != 0 else 0,
                                  post['likes']['count'] / user_friends_count if user_friends_count != 0 else 0,
                                  post['reposts']['count'] / user_friends_count if user_friends_count != 0 else 0,
                                  share_count, reposted_from, attachments))
            if len(user_posts) < 100:
                posts_are_in_time_interval = False
            offset += 100
        return posts

    def __parse_attachments(self, post_attachments):
        attachments = []
        share_count = None
        for attachment in post_attachments:
            if attachment['type'] == 'photo':
                att = attachment['photo']
                attachments.append(dict(type='photo', url=att['photo_604']))
            elif attachment['type'] == 'link':
                att = attachment['link']
                url = att['url']
                attachments.append(dict(type='link', title=att['title'], url=url))
                share_count = self.__get_share_count(url)
        return str(attachments), share_count
