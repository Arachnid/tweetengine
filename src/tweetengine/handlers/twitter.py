import urlparse

from google.appengine.api import users

from tweetengine.handlers import base
from tweetengine import model
from tweetengine import oauth


class TweetHandler(base.BaseHandler):
    @base.requires_account
    def post(self, account_name):
        permission = self.current_permission
        tweet = model.OutgoingTweet(account=self.current_account,
                                    user=self.user_account,
                                    message=self.request.get("tweet"))
        if permission:
            tweet.approved_by=self.user_account
            response = tweet.send()
            if response.status_code != 200:
                self.error(500)
                logging.error(response.content)
        else:
            tweet.put()
        self.redirect("/%s/" % (account_name,))
