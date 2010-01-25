from tweetengine.handlers import base
from tweetengine import model

class ManageHandler(base.UserHandler):
    @base.requires_account
    def get(self, current_account):
        self.render_template("me.html")
