from google.appengine.api import users

from tweetengine.handlers import base
from tweetengine import model


class MeHandler(base.BaseHandler):
  @base.requires_login
  def get(self):
    user = users.get_current_user()
    permissions = model.Permission.all().filter('user =', user).fetch(100)
    self.render_template("me.html", {"permissions": permissions})
