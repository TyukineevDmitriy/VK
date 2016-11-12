class User:
    def __init__(self, id, first_name, last_name, photo, is_member):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.is_member = is_member

class Post:
    def __init__(self, post_id, user_id, text, attachments):
        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        self.attachments = attachments