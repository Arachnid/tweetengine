import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from chameleon.zpt.loader import TemplateLoader

from tweetengine import model
from tweetengine.menu import mainmenu

tpl_path = os.path.join(os.path.dirname(__file__), "..", "templates")
tpl_loader = TemplateLoader(tpl_path, auto_reload=True)

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
        self.current_permission = model.Permission.find(self.user_account,
                                                        self.current_account)
        if not self.current_account:
            self.redirect('/')
        else:
            return func(self, account_name, *args, **kwargs)
    return decorate


def requires_account_admin(func):
    """A decorator that requires a logged in user who admins the current account."""
    @requires_account
    def decorate(self, account_name, *args, **kwargs):
        if not self.current_permission or self.current_permission.role != model.ROLE_ADMINISTRATOR:
            self.error(403)
        else:
            return func(self, account_name, *args, **kwargs)
    return decorate

class BaseHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        self.current_account = None
        self.current_permission = None
        super(BaseHandler, self).initialize(request, response)
        self.user = users.get_current_user()
        if self.user:
            self.user_account = model.GoogleUserAccount.get_or_insert(
                self.user.user_id(),
                user=self.user)
            
    def render_template(self, template_file, template_vars=None):
        if not template_vars:
            template_vars = {}
        if not 'current_account' in template_vars:
            template_vars['current_account'] = None
        template_vars['mainmenu'] = mainmenu(self)
        tpl = tpl_loader.load('base.pt')
        template_vars['master'] = tpl.macros['master']
        tpl = tpl_loader.load(template_file)
        self.response.out.write(tpl(**template_vars))


class UserHandler(BaseHandler):
    def render_template(self, template_path, template_vars=None):
        if not template_vars:
            template_vars = {}
        permissions = self.user_account.permission_set.fetch(100)
        my_acct_keys = set(x.account.key() for x in permissions)
        public_accts = model.TwitterAccount.all().filter("public =", True).fetch(100)
        public_accts = [x for x in public_accts
                        if x.key() not in my_acct_keys]
        logging.warn(public_accts)
        template_vars.update({
            "permissions": permissions,
            "public_accounts": public_accts,
            "current_account": self.current_account,
            "current_permission": self.current_permission,
            "logout_url": users.create_logout_url("/"),
            "user": users.get_current_user(),
            "is_admin": users.is_current_user_admin(),            
        })
        super(UserHandler, self).render_template(template_path, template_vars)
