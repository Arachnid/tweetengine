from google.appengine.ext import db
from google.appengine.ext import polymodel


class UserAccount(polymodel.PolyModel):
  pass


class GoogleUserAccount(UserAccount):
  user = db.UserProperty(required=True)


class TwitterAccount(db.Model):
  username = db.StringProperty(required=True)


ROLE_USER = 1
ROLE_ADMINISTRATOR = 2


class Permission(db.Model):
  user = db.ReferenceProperty(UserAccount, required=True)
  account = db.ReferenceProperty(TwitterAccount, required=True)
  role = db.IntegerProperty(required=True,
                            choices=[ROLE_USER, ROLE_ADMINISTRATOR])


class OutgoingTweet(db.Model):
  account = db.ReferenceProperty(TwitterAccount, required=True)
  user = db.ReferenceProperty(UserAccount, required=True)
  approved_by = db.ReferenceProperty(UserAccount, required=True)
  message = db.TextProperty(required=True)
  timestamp = db.DateTimeProperty(required=True, auto_now_add=True)
