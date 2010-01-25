from google.appengine.ext import webapp

import handlers


application = webapp.WSGIApplication([
    ('/', handlers.HomepageHandler),
], debug=True)