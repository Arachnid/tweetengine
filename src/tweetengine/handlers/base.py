import os
import tenjin
from tenjin.helpers import *

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from tweetengine import model
from tweetengine.menu import mainmenu

shared_cache = tenjin.GaeMemcacheCacheStorage()
tengine = tenjin.Engine(cache=shared_cache)

def requires_login(func):
    def decorate(self, *args, **kwargs):
        if not self.user:
            self.redirect(users.create_login_url(self.request.url))
        else:
            return func(self, *args, **kwargs)
    return decorate


def requires_admin(func):
    def decorate(self, *args, **kwargs):
        if not self.user:
            self.redirect(users.create_login_url(self.request.url))
        elif not users.is_current_user_admin():
            self.error(403)
        else:
            return func(self, *args, **kwargs)
    return decorate


def requires_account(func):
    """A decorator that requires a logged in user and a current account."""
    @requires_login
    def decorate(self, account_name, *args, **kwargs):
        self.current_account = model.TwitterAccount.get_by_key_name(account_name)
        if not self.current_account:
            self.redirect('/')
        else:
            return func(self, account_name, *args, **kwargs)
    return decorate


def requires_account_admin(func):
    """A decorator that requires a logged in user who admins the current account."""
    @requires_account
    def decorate(self, account_name, *args, **kwargs):
        q = model.Permission.all()
        q.filter("account =", self.current_account)
        q.filter("user =", self.user_account)
        q.filter("role =", model.ROLE_ADMINISTRATOR)
        self.account_admin = q.get()
        if not self.account_admin:
            self.error(403)
        else:
            return func(self, account_name, *args, **kwargs)
    return decorate


class BaseHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        self.current_account = None
        super(BaseHandler, self).initialize(request, response)
        self.user = users.get_current_user()
        if self.user:
            self.user_account = model.GoogleUserAccount.get_or_insert(
                self.user.user_id(),
                user=self.user)

    def render_template(self, template_path, template_vars=None):
        if not template_vars:
            template_vars = {}
        template_vars['mainmenu'] = mainmenu(self)
        path = os.path.join(os.path.dirname(__file__), "..", "templates",
                                                template_path)
        self.response.out.write(template.render(path, template_vars))


class UserHandler(BaseHandler):
    def render_template(self, template_path, template_vars=None):
        if not template_vars:
            template_vars = {}
        permissions = model.Permission.all().filter('user =', 
                                                self.user_account).fetch(100)
        template_vars.update({
            "permissions": permissions,
            "current_account": self.current_account,
            "logout_url": users.create_logout_url("/"),
            "mainmenu": mainmenu(self),
            "user": users.get_current_user(),
            "is_admin": users.is_current_user_admin(),
        })
        super(UserHandler, self).render_template(template_path, template_vars)
