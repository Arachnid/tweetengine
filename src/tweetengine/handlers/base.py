import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


def requires_login(func):
  def decorate(self, *args, **kwargs):
    if not users.get_current_user():
      self.redirect(users.create_login_url(self.request.url))
    else:
      return func(self, *args, **kwargs)
  return decorate


class BaseHandler(webapp.RequestHandler):
  def render_template(self, template_path, template_vars=None):
    if not template_vars:
      template_vars = {}
    path = os.path.join(os.path.dirname(__file__), "..", "templates",
                        template_path)
    self.response.out.write(template.render(path, template_vars))
