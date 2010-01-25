import logging
from google.appengine.api import users
from tweetengine.handlers import base
from tweetengine.model import Configuration

class SettingsHandler(base.BaseHandler):
    
    def get(self):
        if not users.is_current_user_admin:
            self.error(403)
            return        
        cfg = Configuration.instance()
        self.render_template("settings.html", {'saved': False, 'cfg': cfg})
        
    def post(self):
        if not users.is_current_user_admin:
            self.error(403)
            return
        saved = False
        logging.info(self.request.params)
        cfg = Configuration.instance()
        params = self.request.params
        if params.get('settings', False):
            cfg.oauth_secret = params.get('twitterapisecret')
            cfg.oauth_key = params.get('twitterapikey')
            cfg.put()
            logging.info('Global settings changed!')
            saved = True
        if params.get('settings.cancel', False):
            self.redirect('/')
            return
        self.render_template("settings.html", {'saved': saved, 'cfg': cfg})