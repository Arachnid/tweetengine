from google.appengine.api import users

from tweetengine.handlers import base
from tweetengine import model

class HomepageHandler(base.UserHandler):
    def get(self):
        if self.user:
            permission = self.user_account.permission_set.get()
            if permission:
                self.redirect("/%s/" % (permission.account.username,))
            else:
                self.render_template("gettingstarted.pt")
        else:
            main_url = users.create_login_url("/")
            self.render_template("index.pt", {"main_url": main_url})
