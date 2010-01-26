from tweetengine import model
from google.appengine.api import users

def setConfiguration():
    account_name='tweet_engine'
    password='passwd'
    oauth_key='fookey'
    oauth_secret='foosecret'



    conf = model.Configuration.instance()
    conf.oauth_key = oauth_key
    conf.oauth_secret = oauth_secret
    conf.put()

def addTwitterAccounts():
    account = model.TwitterAccount.get_or_insert(
        'tweet_engine',
        oauth_token='usertoken',
        oauth_secret='usersecret',
        name='Full name',
        picture='')
    account.put()

def addUsers():
    user_data = (('test1@example.org', 1),
             ('test2@example.org', 2))
    for email, role in user_data:
        user = users.User(email=email)
        usr = model.GoogleUserAccount(user=user)
        usr.put()
        
    permission = model.Permission(
        user=usr,
        account=model.TwitterAccount.get_by_key_name('tweet_engine'),
        role=model.ROLE_ADMINISTRATOR)
    permission.put()
