import os
from setuptools import setup, find_packages

setup(
    name="tweetengine",
    version='1.0',
    package_dir = {'':'src'},
    packages=find_packages('src'),
    zip_safe = True,
    include_package_data = False,
    install_requires = [# defines this in buildout 
    ],
    extras_require = dict(test=['zope.testing', 'webtest']),
)
