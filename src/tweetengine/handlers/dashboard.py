from tweetengine.handlers import base
from tweetengine import model

class DashboardHandler(base.UserHandler):
    @base.requires_login
    def get(self):
        self.render_template("me.html")