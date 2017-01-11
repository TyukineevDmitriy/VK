import ast
from gunstar.http import *
from web.db_config import DBConfig


class IndexHandler(RequestHandler):

    def get(self):
        db_config = DBConfig()
        members = db_config.get_members()
        self.render_template('index.html', members=members)


class OtherHandler(RequestHandler):

    def get(self, user_id):
        db_config = DBConfig()
        user = db_config.get_user(user_id)
        self.render_template('news_feed.html', user=user)

    def post(self, user_id):
        db_config = DBConfig()
        user = db_config.get_user(user_id)
        sorting = self.request.POST.get('sorting', None)
        news_feed = db_config.get_sorted_news_feed(user, sorting)
        for post in news_feed:
            if post.attachments is not None:
                post.attachments = ast.literal_eval(post.attachments)
        self.render_template('news_feed.html', user=user, news_feed=news_feed)