import os
from google.appengine.api import users

def webapp_add_wsgi_middleware(app):
    from appstats import recording
    app = recording.appstats_wsgi_middleware(app)
    return app
