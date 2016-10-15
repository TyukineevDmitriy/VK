from vk_requests import *
import datetime

class Newsticker:

    def __init__(self, number):
        vk_requests = Vk_requests()
        members = vk_requests.get_members()
        friends = vk_requests.get_all_friends_async(members)
        posts = vk_requests.get_friends_posts_async(friends.get(number))
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
                date = datetime.datetime.fromtimestamp(int(post["date"])).strftime('%Y-%m-%d %H:%M:%S')
                self.newsticker.append({"name":friend["first_name"] + " " + friend["last_name"],"avatar":friend["avatar"],
                                   "text":post["text"],"likes":post["likes"],"reposts":post["reposts"],
                                   "comments":post["comments"],"photo":photo,"audio":audio,"post_reference":post_reference,
                                   "date":date})

    def sort_by_likes(self):
        self.newsticker.sort(key=lambda x: x["likes"]["count"],reverse=True)

    def sort_by_reposts(self):
        self.newsticker.sort(key=lambda x: x["reposts"]["count"],reverse=True)

    def sort_by_comments(self):
        self.newsticker.sort(key=lambda x: x["comments"]["count"],reverse=True)

    def get_posts_count(self):
        return len(self.newsticker)