from google.appengine.api import users

from tweetengine.handlers import base
from tweetengine import model
from tweetengine import oauth


class MeHandler(base.BaseHandler):
    @base.requires_login
    def get(self):
        user = users.get_current_user()
        permissions = model.Permission.all().filter('user =', user).fetch(100)
        self.render_template("me.html", {"permissions": permissions})


class AddHandler(base.BaseHandler):
    @base.requires_login
    def get(self):
        config = model.Configuration.instance()
        client = oauth.TwitterClient(config.key, config.secret, "/_oauth/callback")
        