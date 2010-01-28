import logging
from google.appengine.api import urlfetch
from tweetengine.handlers import base
from tweetengine import model

ALLOWED_ENDPOINTS = dict()
ALLOWED_ENDPOINTS['public'] = { 'mytweets': 'statuses/user_timeline', 
                                'mentions': 'statuses/mentions'}
ALLOWED_ENDPOINTS['private'] = {'mytweets': 'statuses/user_timeline', 
                                'friends' : 'statuses/home_timeline', 
                                'mentions': 'statuses/mentions',
                                'direct'  : 'direct_messages'}

class TwitterApiHandler(base.UserHandler):
    @base.requires_account
    def get(self, account_name, listtype):
        if self.current_permission.role == model.ROLE_ANYONE:
            scope = 'public'
        else:
            scope = 'private'
        if listtype not in ALLOWED_ENDPOINTS[scope]:
            self.error(403)
            return
        url = "http://twitter.com/%s.json" % ALLOWED_ENDPOINTS[scope][listtype]
        response = self.current_account.make_request(
            url, method=urlfetch.GET, additional_params=self.request.GET)
        logging.warn(response.status_code)
        self.response.headers['Content-Type'] = response.headers['Content-Type']
        self.response.set_status(response.status_code)
        self.response.out.write(response.content)