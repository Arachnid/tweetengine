import os
from google.appengine.ext import webapp
from tweetengine import handlers
import tweetengine.i18n

TWITTER_RE = '/([a-zA-Z0-9_]+)/'

application = webapp.WSGIApplication([
        ('/', handlers.HomepageHandler),
        (TWITTER_RE, handlers.DashboardHandler),
        (TWITTER_RE+'manage', handlers.ManageHandler),
        (TWITTER_RE+'manage_users', handlers.ManageUsersHandler),
        (TWITTER_RE+'invite', handlers.InviteHandler),
        (TWITTER_RE+'tweet', handlers.TweetHandler),
        (TWITTER_RE+'api/(.*).json', handlers.TwitterApiHandler),
        ('/add/callback', handlers.CallbackHandler),
        ('/add', handlers.AddHandler),
        ('/admin', handlers.SettingsHandler),
        ('/_ah/xmpp/message/chat/', handlers.XMPPHandler),
], debug=os.environ['SERVER_SOFTWARE'].startswith('Dev'))