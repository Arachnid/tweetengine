import environment
import datetime
import logging
import time
import urlparse

from google.appengine.api import users

from tweetengine.handlers import base
from tweetengine import model
from tweetengine import oauth

class TweetHandler(base.BaseHandler):
    @base.requires_account
    def post(self, account_name):
        permission = self.current_permission
        in_reply_to = self.request.get("in_reply_to_status_id", None)
        tweet = model.OutgoingTweet(account=self.current_account,
                                    user=self.user_account,
                                    message=self.request.get("tweet"),
                                    in_reply_to=in_reply_to)
        if permission.can_send():
            tweet.approved_by=self.user_account
            tweet.approved = True
            if self.request.POST["when"] == "schedule":
                timestamp = "%s %s" % (self.request.POST['datestamp'],
                                       self.request.POST['timestamp'])
                tweet.timestamp = datetime.datetime.strptime(timestamp,"%d/%m/%Y %H:%M")
                tweet.schedule()
            else:
                response = tweet.send()
                if response.status_code != 200:
                    self.error(500)
                    logging.error(response.content)
        elif permission.can_suggest():
            tweet.put()
        self.redirect("/%s/" % (account_name,))


def publishApprovedTweets():
    q = model.OutgoingTweet.all()
    q.filter("approved =", True)
    q.filter("sent =", False)
    q.filter("timestamp <", datetime.datetime.now())
    rpcs = []
    for tweet in q.fetch(30):
        rpcs.append((tweet.send_async(), tweet))
        logging.error('sending tweet %s' % tweet.message)
        
    successful_tweets = []
    for rpc, tweet in rpcs:
        response = rpc.get_result()
        if response.status_code == 200:
            successful_tweets.append(tweet)
        else:
            logging.error(response.content)
    db.put(successful_tweets)

            
