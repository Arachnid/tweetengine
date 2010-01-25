from google.appengine.ext import webapp

from tweetengine import handlers


application = webapp.WSGIApplication([
        ('/', handlers.HomepageHandler),
        ('/([a-zA-Z_]+)/', handlers.DashboardHandler),
        ('/([a-zA-Z_]+)/manage', handlers.ManageHandler),
        ('/add/callback', handlers.CallbackHandler),
        ('/add', handlers.AddHandler),
        ('/admin', handlers.SettingsHandler),
        ('/([a-zA-Z_]+)/tweet', handlers.TweetHandler),
], debug=True)

