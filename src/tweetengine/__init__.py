from google.appengine.ext import webapp

from tweetengine import handlers


application = webapp.WSGIApplication([
        ('/', handlers.HomepageHandler),
        ('/me/', handlers.MeHandler),
], debug=True)