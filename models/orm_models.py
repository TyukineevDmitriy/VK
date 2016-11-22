from peewee import *
from playhouse.db_url import connect

#db = MySQLDatabase('vkdb',user'mysql://root:semechki@192.168.1.34:3306/vkdb')
db = MySQLDatabase('vkdb',user='root', passwd='semechki', host='localhost', port=3306)

def create_tables():
    db.connect()
    db.create_tables([User, Friend, Post], True)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = IntegerField(primary_key=True)
    first_name = CharField()
    last_name = CharField()
    photo = CharField()
    is_member = BooleanField()

class Friend(BaseModel):
    user = ForeignKeyField(User, related_name='friend_rel_user', db_column='user')
    friend = ForeignKeyField(User, related_name='friend_rel_friend', db_column='friend')
    class Meta:
        primary_key = CompositeKey('user', 'friend')
        indexes = (
            (('user', 'friend'), True),
        )

class Post(BaseModel):
    user = ForeignKeyField(User, related_name='post_rel_user', db_column='user')
    post_id = IntegerField()

    class Meta:
        primary_key = CompositeKey('user', 'post_id')