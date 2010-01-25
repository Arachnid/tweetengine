import urlparse

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
        callback_url = urlparse.urljoin(self.request.url, "/_oauth/callback")
        client = oauth.TwitterClient(config.oauth_key, config.oauth_secret,
                                     callback_url)
        self.redirect(client.get_authorization_url())


class CallbackHandler(base.BaseHandler):
    @base.requires_login
    def get(self):
        config = model.Configuration.instance()
        client = oauth.TwitterClient(config.oauth_key, config.oauth_secret,
                                     callback_url)
        auth_token = self.request.get("oauth_token")
        auth_verifier = self.request.get("oauth_verifier")
        user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
        