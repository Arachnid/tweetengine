from google.appengine.api import users
from tweetengine import model
from tweetengine.i18n import translate
from tweetengine.i18n import _

class MenuItem(object):
    
    def __init__(self, name, func):
        self.name = name
        self.func = func
        
    def __call__(self, handler):
        item = result = self.func(handler)
        if not item['visible']:
            return u''
        item['name'] = translate(self.name, context=handler.request)
        item['attr'] = ''
        if item['active']:
            item['attr'] = u'class="active"'
        markup = u'<li %(attr)s><a href="%(url)s">%(name)s</a></li>'
        return markup % item
        
class Menu(object):

    def __init__(self):
        self.items = list()
    
    def add(self, name, func):
        self.items.append(MenuItem(name, func))

    def __call__(self, handler):
        markup = u'<ul>\n'   
        for item in self.items:
            markup += item(handler)
        markup += u'</ul>\n' 
        return markup  
    
mainmenu = Menu()

def home(handler):
    if not handler.user:
        return dict(visible=True, active=True, url="/")
    else:
        return dict(visible=False, active=False, url="/")

mainmenu.add(_("home"), home)

def login(handler):
    if not handler.user:
        return dict(visible=True, active=False, 
                    url=users.create_login_url("/"))
    return dict(visible=False, active=False, url='')
    
mainmenu.add(_('login'), login)

def dashboard(handler):
    import tweetengine.handlers
    if not handler.user or not handler.current_account and \
       not isinstance(handler, tweetengine.handlers.SettingsHandler):
        return dict(visible=False, active=False, url='')
    active = isinstance(handler, tweetengine.handlers.DashboardHandler)
    url = '/'
    if not isinstance(handler, tweetengine.handlers.SettingsHandler):
        url = '/%s/' % handler.current_account.username
    return dict(visible=True, active=active, url=url)

mainmenu.add(_('dashboard'), dashboard)

def manage(handler):
    if not handler.user or not handler.current_account:
        return dict(visible=False, active=False, url='')
    if not handler.current_permission or handler.current_permission.role != model.ROLE_ADMINISTRATOR:
        return dict(visible=False, active=False, url='')
    import tweetengine.handlers
    active = isinstance(handler, tweetengine.handlers.ManageHandler)
    url = '/%s/manage' % handler.current_account.username
    return dict(visible=True, active=active, url=url)

mainmenu.add(_('manage'), manage)

def admin(handler):
    if not users.is_current_user_admin():
        return dict(visible=False, active=False, url='')
    import tweetengine.handlers
    active = isinstance(handler, tweetengine.handlers.SettingsHandler)
    return dict(visible=True, active=active, url='/admin')

mainmenu.add(_('admin'), admin)

def logout(handler):
    if handler.user:                
        return dict(visible=True, active=False, 
                    url=users.create_logout_url("/"))
    return dict(visible=False, active=False, url='')    

mainmenu.add(_('logout'), logout)