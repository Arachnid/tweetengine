from tweetengine import model
from google.appengine.api import users
from google.appengine.ext.webapp import xmpp_handlers

class XMPPHandler(xmpp_handlers.BaseHandler):
    def message_received(self, message):
        twitter_account = model.TwitterAccount.get_by_key_name(message.to.split("@")[0])
        user = users.User(message.sender.split('/')[0])
        user_account = model.GoogleUserAccount.all().filter("user =", user).get()
        if not user_account or not twitter_account:
            self.not_allowed(message)
            return
        permission = model.Permission.find(user_account, twitter_account)
        tweet = model.OutgoingTweet(account=twitter_account,
                                    user=user_account,
                                    message=message.body)
        if permission.can_send() or permission.can_suggest():
            tweetlen = len(message.body)
            if tweetlen > 140:
                self.too_long(message, tweetlen)
                return
        if permission.can_send():
            tweet.approved_by = user_account
            response = tweet.send()
            if response.status_code != 200:
                self.internal_error(message)
                logging.error(response.content)
                return
            self.sent(message)
        elif permission.can_suggest():
            tweet.put()
            self.submitted(message)
        else:
            self.not_allowed(message)

    def not_allowed(self, message):
        message.reply("You are not allowed to submit or suggest tweets for this account.")

    def internal_error(self, message):
        message.reply("An internal error occurred trying to send your tweet. Please try again later.")

    def sent(self, message):
        message.reply("Tweet sent!")

    def submitted(self, message):
        message.reply("Your tweet has been submitted for review.")

    def too_long(self, message, tweetlen):
        message.reply("Tweet too long: You sent %d characters, max is 140." % (tweetlen,))
