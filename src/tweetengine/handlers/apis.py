import logging
from google.appengine.api import urlfetch
from tweetengine.handlers import base
from tweetengine import model

ALLOWED_ENDPOINTS = set(["statuses/user_timeline", 
                         "statuses/friends_timeline", 
                         "statuses/mentions",
                         "direct_messages"])

class TwitterApiHandler(base.UserHandler):
    @base.requires_account
    def get(self, account_name, endpoint):
        if endpoint not in ALLOWED_ENDPOINTS:
            self.error(403)
            return
        url = "http://twitter.com/%s.json" % endpoint
        response = self.current_account.make_request(
            url, method=urlfetch.GET, additional_params=self.request.GET)
        logging.warn(response.status_code)
        self.response.headers['Content-Type'] = response.headers['Content-Type']
        self.response.set_status(response.status_code)
        self.response.out.write(response.content)
