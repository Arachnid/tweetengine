import os
import tenjin
from tenjin.helpers import *

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from tweetengine import model

shared_cache = tenjin.GaeMemcacheCacheStorage()
tengine = tenjin.Engine(cache=shared_cache)

def requires_login(func):
    def decorate(self, *args, **kwargs):
        if not self.user:
            self.redirect(users.create_login_url(self.request.url))
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

class Menu(object):

    def __init__(self):
        self.keys = list()
        self.items = dict()
    
    def add(self, name, url):
        if name in self.keys:
            raise ValueError, "Name already registered"
        self.keys.append(name)
        self.items[name] = {'name': name, 'url': url, 'active': False}

    def activate(self, name):
        self.items[name]['active'] = True
        
    @property
    def rendered(self):   
        path = os.path.join(os.path.dirname(__file__), "..", "templates",
                            'menu.html')     
        return tengine.render(path, {'menu': self})
    
    def __iter__(self):
        def _iterator():
            for key in self.keys:
                yield self.items[key]
        return _iterator()

class BaseHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        self.menu = Menu()
        super(BaseHandler, self).initialize(request, response)
        self.user = users.get_current_user()
        if self.user:
            self.user_account = model.GoogleUserAccount.get_or_insert(
                self.user.user_id(),
                user=self.user)
        self.init_menu()
            
    def init_menu(self):
        if not self.user:
            self.menu.add('login', users.create_login_url("/me/"))
        else:
            self.menu.add('dashboard', '/')
            self.menu.add('manage', '#')
            if users.is_current_user_admin():
                 self.menu.add('admin', '/admin')
            self.menu.add('logout', users.create_logout_url("/"))

    def render_template(self, template_path, template_vars=None):
        if not template_vars:
            template_vars = {}
        template_vars['menu'] = self.menu
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
        })
        super(UserHandler, self).render_template(template_path, template_vars)
