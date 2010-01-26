import logging
from django import newforms as forms
from google.appengine.api import users
from tweetengine.handlers import base
from tweetengine.model import Configuration

class AdminForm(forms.Form):
    oauth_key = forms.CharField()
    oauth_secret = forms.CharField()


class SettingsHandler(base.BaseHandler):
    @base.requires_admin
    def get(self):
        cfg = Configuration.instance()
        form = AdminForm(initial={
                "oauth_key": cfg.oauth_key,
                "oauth_secret": cfg.oauth_secret
        })
        self.render_template("settings.html", {'form': form})
        
    @base.requires_admin
    def post(self):
        form = AdminForm(self.request.POST)
        saved = False
        if form.is_valid():
            cfg = Configuration.instance()
            cfg.oauth_key = form.clean_data['oauth_key']
            cfg.oauth_secret = form.clean_data['oauth_secret']
            cfg.put()
            saved = True
        self.render_template("settings.html", {'form': form, 'saved': saved})
