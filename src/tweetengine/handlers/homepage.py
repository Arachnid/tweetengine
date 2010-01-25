import base

class HomepageHandler(base.BaseHandler):
  def get(self):
    self.render_template("index.html")
