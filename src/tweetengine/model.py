import datetime
import time
from google.appengine.api import urlfetch
from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from tweetengine import oauth

class UserAccount(polymodel.PolyModel):
    def get_username(self):
        raise NotImplementedError()


class GoogleUserAccount(UserAccount):
    user = db.UserProperty(required=True)

    def get_username(self):
        return self.user.email()


ROLE_ANYONE = 0
ROLE_USER = 1
ROLE_ADMINISTRATOR = 2

ROLES = [
    (ROLE_ANYONE, "Anyone"),
    (ROLE_USER, "User"),
    (ROLE_ADMINISTRATOR, "Administrator")
]
ROLE_IDS = [id for id,name in ROLES]


class TwitterAccount(db.Model):
    oauth_token = db.TextProperty(required=True)
    oauth_secret = db.TextProperty(required=True)
    name = db.TextProperty()
    picture = db.TextProperty()
    
    # Permission levels
    suggest_tweets = db.IntegerProperty(required=True, choices=ROLE_IDS,
                                        default=ROLE_ANYONE)
    send_tweets = db.IntegerProperty(required=True, choices=ROLE_IDS,
                                     default=ROLE_USER)
    review_tweets = db.IntegerProperty(required=True, choices=ROLE_IDS,
                                       default=ROLE_USER)

    @property
    def username(self):
        return self.key().name()

    def make_async_request(self, url, additional_params=None, method=urlfetch.POST):
        client = Configuration.instance().get_client("")
        return client.make_async_request(
            url,
            token=self.oauth_token,
            secret=self.oauth_secret,
            additional_params=additional_params,
            protected=True,
            method=method)

    def make_request(self, url, additional_params=None, method=urlfetch.POST):
        return self.make_async_request(url, additional_params, method).get_result()
    
    def prepare_request(self, url, additional_params=None, 
                        method=urlfetch.GET):
        client = Configuration.instance().get_client("")
        return client.prepare_request(
            url,
            token=self.oauth_token,
            secret=self.oauth_secret,
            additional_params=additional_params,
            method=method)


def _normalize_key_name(key):
    if isinstance(key, db.Model):
        key = key.key()
    if isinstance(key, db.Key):
        key = key.id_or_name()
    return key


class Permission(db.Model):
    user = db.ReferenceProperty(UserAccount, required=True)
    account = db.ReferenceProperty(TwitterAccount, required=True)
    role = db.IntegerProperty(required=True,
                              choices=ROLE_IDS)
    invite_nonce = db.StringProperty()

    @classmethod
    def create(cls, user, account, role, invite_nonce=None):
        user_name = _normalize_key_name(user)
        account_name = _normalize_key_name(account)
        key_name = "%s:%s" % (user_name, account_name)
        return cls(
            key_name=key_name,
            user=user,
            account=account,
            role=role,
            invite_nonce=invite_nonce)

    @classmethod
    def find(cls, user, account):
        user_name = _normalize_key_name(user)
        account_name = _normalize_key_name(account)
        key_name = "%s:%s" % (user_name, account_name)
        permission = cls.get_by_key_name(key_name)
        if not permission:
            permission = cls(user=user, account=account, role=ROLE_ANYONE)
        return permission

    def can_suggest(self):
        return self.role >= self.account.suggest_tweets
    
    def can_send(self):
        return self.role >= self.account.send_tweets
    
    def can_review(self):
        return self.role >= self.account.review_tweets


class OutgoingTweet(db.Model):
    account = db.ReferenceProperty(TwitterAccount, required=True)
    user = db.ReferenceProperty(UserAccount, required=True,
                                collection_name='tweets')
    approved_by = db.ReferenceProperty(UserAccount,
                                       collection_name='approved_tweets')
    message = db.TextProperty(required=True)
    timestamp = db.DateTimeProperty()
    sent = db.BooleanProperty(required=True, default=False)
    approved = db.BooleanProperty(required=True, default=False)
    in_reply_to = db.StringProperty()

    @property
    def date(self):
        if self.timestamp:
            return self.timestamp.strftime("%d/%m/%Y")
        return ''

    @property
    def time(self):
        if self.timestamp:
            return self.timestamp.strftime("%H:%M")
        return ''
    
    def send_async(self):
        rpc = self.account.make_async_request(
            "http://twitter.com/statuses/update.json",
            additional_params={
                "status": self.message,
                "in_reply_to_status_id": self.in_reply_to})
        self.approved = True
        self.sent = True
        self.timestamp = datetime.datetime.now()
        return rpc

    def send(self):
        response = self.send_async().get_result()
        if respones.status_code == 200:
            self.put()
        return response
    
    def schedule(self):
        from tweetengine.handlers import twitter
        task_name = 'tweet-%d' % (time.mktime(self.timestamp.timetuple())/300)
        try:
            taskqueue.Task(eta=self.timestamp, name=task_name,
                           url=twitter.ScheduledTweetHandler.URL_PATH).add()
        except taskqueue.TaskAlreadyExistsError:
            pass
        self.put()
        

class Configuration(db.Model):
    INSTANCE = None
    
    oauth_secret = db.StringProperty()
    oauth_key = db.StringProperty()
    mail_from = db.StringProperty()
    allow_public = db.BooleanProperty(required=True, default=False)
    
    @classmethod
    def instance(cls):
        if not cls.INSTANCE:
            cls.INSTANCE = cls.get_or_insert('oauthkey')
        return cls.INSTANCE

    def get_client(self, callback_url):
        return oauth.TwitterClient(self.oauth_key, self.oauth_secret,
                                   callback_url)
