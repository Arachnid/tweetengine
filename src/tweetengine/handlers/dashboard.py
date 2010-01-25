from tweetengine.handlers import base
from tweetengine import model

class DashboardHandler(base.UserHandler):
    @base.requires_account
    def get(self, account_name):
        self.menu.activate('dashboard')
        self.render_template("me.html")