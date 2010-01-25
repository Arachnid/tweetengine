from google.appengine.ext import webapp

from tweetengine import handlers


application = webapp.WSGIApplication([
        ('/', handlers.HomepageHandler),
        ('/[a-zA-Z_]+/', handlers.DashboardHandler),
        ('/add/callback', handlers.CallbackHandler),
        ('/add', handlers.AddHandler),
], debug=True)