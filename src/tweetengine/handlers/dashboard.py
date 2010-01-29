import datetime
import logging
import time
from google.appengine.ext import db
from google.appengine.ext import deferred
from google.appengine.api.labs import taskqueue
from tweetengine.handlers import base, twitter
from tweetengine.oauth import TwitterClient
from tweetengine import model

class DashboardHandler(base.UserHandler):

    def get_tweets(self):
        if self.current_permission.can_review():
            q = model.OutgoingTweet.all()
            q.filter("account =", self.current_account)
            q.filter("sent =", False)
            return q.fetch(20)
        else:
            return []

    @base.requires_account
    def get(self, account_name):        
        self.render_template("dashboard.pt", {
            "tweets": self.get_tweets(),
        })

    @base.requires_account
    def post(self, account_name):
        if not self.current_permission.can_review():
            self.error(403)
            return
        tweets = self.get_tweets()
        tweet_map = dict((x.key().id(), x) for x in tweets)

        # Delete marked for deletion
        to_delete = [tweet_map[int(k.split(".")[1])]
                     for k, v in self.request.POST.iteritems()
                     if k.startswith("tweet.") and v=='delete']
        db.delete(to_delete)


        for k, v in self.request.POST.iteritems():
            if k.startswith("tweet.") and v=='send':
                tweet = tweet_map[int(k.split(".")[1])]
                tweet.approved_by = self.user_account
                tweet.approved = True
                timestamp = "%s %s" % (self.request.POST['datestamp.%s' % tweet.key().id()],
                                       self.request.POST['timestamp.%s' % tweet.key().id()])
                now = datetime.datetime.now()
                if timestamp:
                    tweet.timestamp = datetime.datetime.strptime(timestamp,"%d/%m/%Y %H:%M")                
                    if tweet.timestamp > now:
                        tweet.put()
                        task_name = 'tweet-%d' % (time.mktime(tweet.timestamp.timetuple())/300)
                        try:
                            deferred.defer(twitter.publishApprovedTweets, _eta=tweet.timestamp,_name=task_name)
                        except taskqueue.TaskAlreadyExistsError:
                            pass
                        # we have postpone the sending, continue to next tweet
                        continue

                # send now
                response = tweet.send()
                if response.status_code != 200:
                    self.error(500)
                    logging.error(response.content)

        self.redirect('/%s/' % account_name)
