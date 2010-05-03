TweetEngine
===========

TweetEngine is a tool for collaborative twittering. It allows a degree of 
control who tweets what including reviews. 

TweetEngine is build on/for Googles Appengine and is Free and OpenSource 
Software under the Apache Public License 2.0.

It was written at Snowsprint 2010 by Nick Johnson (Google, Ireland), 
Jens W. Klein (BlueDynamics Allaince Austria) and Sasha Vincic (Valentine 
Websystems, Schweden).

The code and bugtracker of TweetEngine is located at github.

http://github.com/Arachnid/tweetengine

If you want to try and install TweetEngine on your own, get the code and 
take a clean Python 2.5. Then do a ``python bootstrap.py``. Next run 
``./bin/buildout``. Then start``./bin/tweetengine`` for you local development 
instance. In your browser go to ``http://localhost:8080``. In case of problems 
consult the zc.buildout and/or Appengine documentation. 

http://www.buildout.org/
https://appengine.google.com

Running the application
========================

The first time you run the application, you will need to configure it. Both on
the local server in in production, this is done by logging in with an admin account.

1. Click on "Admin" - this will take you to a settings page where you can add your 
Twitter API keys. If you don't already have a key, sign up for one at 
http://dev.twitter.com. Note that you can use any callback or URL you want - Twitter's
application admin page won't let you set localhost:8080 as the callback URL, but
this won't matter since Tweetengine will pass this as an OAuth parameter anyway
when users add an account.

2. From dev.twitter.com, copy "Consumer Key" to your dashboard's "OAuth key", 
"Consumer secret" to "OAuth secret" and set "Mail from" to an email account that
your App Engine account is able to sent email from.  
