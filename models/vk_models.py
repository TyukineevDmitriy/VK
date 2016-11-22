class User:
    def __init__(self, id, first_name, last_name, photo, is_member):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.is_member = is_member

class Post:
    def __init__(self, user_id, post_id, text, date, comments, likes, reposts, reposted_from, attachments):
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.date = date
        self.comments = comments
        self.likes = likes
        self.reposts = reposts
        self.reposted_from = reposted_from
        self.attachments = attachments