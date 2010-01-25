from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from tweetengine import oauth

class UserAccount(polymodel.PolyModel):
    pass


class GoogleUserAccount(UserAccount):
    user = db.UserProperty(required=True)


class TwitterAccount(db.Model):
    oauth_token = db.TextProperty(required=True)
    oauth_secret = db.TextProperty(required=True)
    name = db.TextProperty()
    picture = db.TextProperty()

    @property
    def username(self):
        return self.key().name()

    def make_request(self, url, additional_params=None, method=urlfetch.POST):
        if not additional_params:
            additional_params = {}
        client = Configuration.instance().get_client("")
        return client.make_request(
            url,
            token=self.oauth_token,
            secret=self.oauth_secret,
            additional_params=additional_params,
            protected=True,
            method=method)


ROLE_USER = 1
ROLE_ADMINISTRATOR = 2


class Permission(db.Model):
    user = db.ReferenceProperty(UserAccount, required=True)
    account = db.ReferenceProperty(TwitterAccount, required=True)
    role = db.IntegerProperty(required=True,
                              choices=[ROLE_USER, ROLE_ADMINISTRATOR])


class OutgoingTweet(db.Model):
    account = db.ReferenceProperty(TwitterAccount, required=True)
    user = db.ReferenceProperty(UserAccount, required=True,
                                collection_name='tweets')
    approved_by = db.ReferenceProperty(UserAccount, required=True,
                                       collection_name='approved_tweets')
    message = db.TextProperty(required=True)
    timestamp = db.DateTimeProperty(required=True, auto_now_add=True)
    sent = db.BooleanProperty(required=True, default=False)

    def send(self):
        response = self.account.make_request(
            "http://twitter.com/statuses/update.json",
            additional_params={"status": self.message})
        if response.status_code == 200:
            self.sent = True
            self.put()
        return response


class Configuration(db.Model):
    oauth_secret = db.StringProperty()
    oauth_key = db.StringProperty()
    
    @classmethod
    def instance(cls):
        return cls.get_or_insert('oauthkey')

    def get_client(self, callback_url):
        return oauth.TwitterClient(self.oauth_key, self.oauth_secret,
                                   callback_url)
