from google.appengine.api import users

from tweetengine.handlers import base


class HomepageHandler(base.BaseHandler):
    def get(self):
        if users.get_current_user():
            main_url = "/me/"
        else:
            main_url = users.create_login_url("/me/")
        self.render_template("index.html", {"main_url": main_url})
