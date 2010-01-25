import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from tweetengine import model

def requires_login(func):
    def decorate(self, *args, **kwargs):
        if not self.user:
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


class UserHandler(BaseHandler):
    def initialize(self, request, response):
        super(UserHandler, self).initialize(request, response)
        self.user = users.get_current_user()
        if self.user:
            self.user_account = model.GoogleUserAccount.get_or_insert(
                self.user.user_id(),
                user=self.user)

    def render_template(self, template_path, template_vars=None):
        if not template_vars:
            template_vars = {}
        permissions = model.Permission.all().filter('user =', 
                                                self.user_account).fetch(100)
        template_vars.update({
            "permissions": permissions,
        })
        super(UserHandler, self).render_template(template_path, template_vars)
