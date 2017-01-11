class User:
    def __init__(self, id, first_name, last_name, photo, is_member):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.is_member = is_member

class Post:
    def __init__(self, user_id, post_id, text, date, comments_count,
                 likes_count, reposts_count, normalized_comments,
                 normalized_likes, normalized_reposts, share_count, reposted_from, attachments):
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.date = date
        self.comments_count = comments_count
        self.likes_count = likes_count
        self.reposts_count = reposts_count
        self.normalized_comments = normalized_comments
        self.normalized_likes = normalized_likes
        self.normalized_reposts = normalized_reposts
        self.share_count = share_count
        self.reposted_from = reposted_from
        self.attachments = attachments
