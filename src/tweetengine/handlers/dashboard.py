import logging
from google.appengine.ext import db
from tweetengine.handlers import base
from tweetengine.oauth import TwitterClient
from tweetengine import model

class DashboardHandler(base.UserHandler):

    def get_tweets(self):
        q = model.OutgoingTweet.all()
        q.filter("account =", self.current_account)
        q.filter("sent =", False)

    @base.requires_account
    def get(self, account_name):        
        self.render_template("me.html", {
            "tweets": self.get_tweets(),
            "mentionsurl": self.twitter_api_url('statuses/mentions'),
        })

    @base.requires_account_admin
    def post(self, account_name):
        q = self.get_tweets()
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
                response = tweet.send()
                if response.status_code != 200:
                    self.error(500)
                    logging.error(response.content)

        self.redirect('/%s/' % account_name)

    def twitter_api_url(self, service):
        url = 'http://twitter.com/%s.json' % service
        url, querystring, h, p = self.current_account.prepare_request(url)
        logging.info('%s?%s' % (url, querystring))
        return '%s?%s' % (url, querystring)
