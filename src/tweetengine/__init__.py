from google.appengine.ext import webapp

from tweetengine import handlers


application = webapp.WSGIApplication([
        ('/', handlers.HomepageHandler),
        ('/me/', handlers.MeHandler),
        ('/me/add', handlers.AddHandler),
        ('/_oauth/callback', handlers.CallbackHandler),
], debug=True)