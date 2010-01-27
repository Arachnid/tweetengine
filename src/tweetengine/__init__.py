from google.appengine.ext import webapp

from tweetengine import handlers


application = webapp.WSGIApplication([
        ('/', handlers.HomepageHandler),
        ('/([a-zA-Z_]+)/', handlers.DashboardHandler),
        ('/([a-zA-Z_]+)/manage', handlers.ManageHandler),
        ('/([a-zA-Z_]+)/manage_users', handlers.ManageUsersHandler),
        ('/([a-zA-Z_]+)/invite', handlers.InviteHandler),
        ('/([a-zA-Z_]+)/tweet', handlers.TweetHandler),
        ('/([a-zA-Z_]+)/api/(.*).json', handlers.TwitterApiHandler),
        ('/add/callback', handlers.CallbackHandler),
        ('/add', handlers.AddHandler),
        ('/admin', handlers.SettingsHandler),
], debug=True)

