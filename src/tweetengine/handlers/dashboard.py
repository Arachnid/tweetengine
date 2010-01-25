from tweetengine.handlers import base
from tweetengine import model

class DashboardHandler(base.BaseHandler):
    @base.requires_login
    def get(self):
        permissions = model.Permission.all().filter('user =', 
                                                self.user_account).fetch(100)
        self.render_template("me.html", {"permissions": permissions})