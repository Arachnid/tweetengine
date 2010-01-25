import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class BaseHandler(webapp.RequestHandler):
  def render_template(self, template_path, template_vars=None):
    if not template_vars:
      template_vars = {}
    path = os.path.join(os.path.dirname(__file__), "..", "templates",
                        template_path)
    self.response.out.write(template.render(path, template_vars))
