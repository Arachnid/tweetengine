# it is important that the environmnet module gets imported as the
# very first module in each handler.
import environment
from google.appengine.ext.webapp.util import run_wsgi_app

import tweetengine

def main():
    
    run_wsgi_app(tweetengine.application)

if __name__ == '__main__':
    main()