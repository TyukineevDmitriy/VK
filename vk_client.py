from vk_requests import *
from multiprocessing.dummy import Pool as ThreadPool
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

        '''posts = vk_requests.get_friends_posts_async(friends.get(number))
        self.newsticker = []
        for friend in posts:
            for i in range(len(friend["wall"])):
                #post_reference = ""
                post = friend["wall"][i]
                #if 'copy_history' in friend["wall"][i]:
                post_reference = "https://vk.com/id{0}?w=wall{1}_{2}".format(friend["id"],post["owner_id"],post["id"])
                photo = ""
                audio = ""
                if 'attachments' in post:
                    for attachment in post["attachments"]:
                        if attachment["type"] == "photo":
                            photo = attachment["photo"]["photo_604"]
                        if attachment["type"] == "audio":
                            audio = attachment["audio"]["url"]
                date = datetime.datetime.fromtimestamp(int(post["date"]))
                self.newsticker.append({"name":friend["first_name"] + " " + friend["last_name"],"avatar":friend["avatar"],
                                   "text":post["text"],"likes":post["likes"],"reposts":post["reposts"],
                                   "comments":post["comments"],"photo":photo,"audio":audio,"post_reference":post_reference,
                                   "date":date})'''