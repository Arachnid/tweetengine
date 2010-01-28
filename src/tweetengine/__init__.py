from google.appengine.ext import webapp
import patches
from tweetengine import handlers


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
], debug=True)

# bootstrap the zope zcml crap
import patches
from zope.configuration.xmlconfig import XMLConfig
import zope.component
import zope.i18n
 
XMLConfig('meta.zcml', zope.component)
XMLConfig('configure.zcml', zope.component)
XMLConfig('configure.zcml', zope.i18n)
import tweetengine
XMLConfig('i18n.zcml', tweetengine)

