import os
import unittest, doctest
from zope.testing.doctestunit import DocFileSuite, DocTestSuite
from lovely.gae.testing import DBLayer
from tweetengine import utils

# use the lovely.gae test layer which sets up an in-memory database
# stub, which is cleaned after each test.
dbLayer = DBLayer('DBLayer')

def setup(csl):
    os.environ['SERVER_NAME'] = 'localhost'
    os.environ['SERVER_PORT'] = '8080'
    os.environ['AUTH_DOMAIN'] = 'example.org'
    os.environ['USER_EMAIL'] = 'test2@example.org'
    os.environ['USER_ID'] = 't2'
    utils.setConfiguration()
    utils.addTwitterAccounts()
    utils.addUsers()

def test_suite():
    views = DocFileSuite(
        'views.txt',
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        setUp=setup,
        )
    s = unittest.TestSuite((views,),)
    s.layer = dbLayer
    return s
