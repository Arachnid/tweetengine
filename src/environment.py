"""This module sets up the python path and preloads modules and sets up i18n"""
import sys
import os
import logging
import pkg_resources

# the root directory of the appengine project
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# the library directory, where the eggs reside
LIB_DIR = os.path.join(PROJECT_DIR, 'packages')

# add any file/directory that is an egg under the packages directory
# to the python path
if os.path.isdir(LIB_DIR):
    _eggpaths = []
    
    for name in os.listdir(LIB_DIR):
        p = os.path.join(LIB_DIR, name)
        if name.endswith('.egg'):            
            _eggpaths.append(p)
    sys.path[0:0] = [p for p in _eggpaths if p not in sys.path]    

from lovely.gae.environment import setUp

# this adds the sdk librarires to the path if not already there
setUp(PROJECT_DIR)

# log the current python path
logging.debug('ENVIRONMENT PATH: %r' % sys.path)
