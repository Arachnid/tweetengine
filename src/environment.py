"""This module sets up the python path and preloads modules"""
import sys
import os
import logging

# the root directory of the appengine project
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# the library directory, where the eggs reside
LIB_DIR = os.path.join(PROJECT_DIR, 'packages')

# add any file/directory that is an egg under the packages directory
# to the python path
if os.path.isdir(LIB_DIR):
    _paths = []
    for name in os.listdir(LIB_DIR):
        if name.endswith('.egg'):
            p = os.path.join(LIB_DIR, name)
            _paths.append(p)
    sys.path[0:0] = [p for p in _paths if p not in sys.path]

from lovely.gae.environment import setUp

# this adds the sdk librarires to the path if not already there
setUp(PROJECT_DIR)

# log the current python path
logging.debug('ENVIRONMENT PATH: %r' % sys.path)
