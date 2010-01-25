import urlparse

from google.appengine.api import users

from tweetengine.handlers import base
from tweetengine import model
from tweetengine import oauth


class AddHandler(base.BaseHandler):
    @base.requires_login
    def get(self):
        config = model.Configuration.instance()
        callback_url = urlparse.urljoin(self.request.url, "/add/callback")
        client = oauth.TwitterClient(config.oauth_key, config.oauth_secret,
                                     callback_url)
        self.redirect(client.get_authorization_url())


class CallbackHandler(base.BaseHandler):
    @base.requires_login
    def get(self):
        config = model.Configuration.instance()
        client = oauth.TwitterClient(config.oauth_key, config.oauth_secret, "")
        auth_token = self.request.get("oauth_token")
        auth_verifier = self.request.get("oauth_verifier")
        user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
        
        # Create the twitter account
        account = model.TwitterAccount.get_or_insert(
            user_info["username"],
            oauth_token=user_info["token"],
            oauth_secret=user_info["secret"],
            name=user_info["name"],
            picture=user_info["picture"])
        # Add the user as an admin of the account
        permission = model.Permission(
            user=self.user_account,
            account=account,
            role=model.ROLE_ADMINISTRATOR)
        permission.put()
        
        self.render_template("added.html", {"account": account})