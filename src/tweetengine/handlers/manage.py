from google.appengine.ext import db
from tweetengine.handlers import base
from tweetengine import model

class ManageHandler(base.UserHandler):
    @base.requires_account_admin
    def get(self, account_name):
        permissions = model.Permission.all().filter("account =", self.current_account).fetch(100)
        self.render_template("manage.html", {"permissions": permissions})

    @base.requires_account_admin
    def post(self, account_name):
        permissions = model.Permission.all().filter("account =", self.current_account).fetch(100)
        permission_map = dict((x.key().id(), x) for x in permissions)
        my_id = self.account_Admin.key().id()
        
        # Handle deletion
        to_delete = [permission_map[x]
                     for x in self.request.POST.getall("delete")
                     if x in permission_map and x != my_id]
        db.delete(to_delete)
        
        # Handle permission changes
        new_permissions = dict((int(k.split(".")[1]), v)
                               for k, v in self.request.POST
                               if k.startswith("permission."))
        to_update = []
        for perm_id, role in new_permissions:
            permission = permission_map[perm_id]
            permission.role = role
            to_update.append(permission)
        db.update(to_update)

        # Handle new users
        for new_user in self.request.POST.getall("username"):
        
        self.redirect(self.url)
