from setuptools import setup, find_packages

version = '1.0'
shortdesc = ''
longdesc = ''

setup(name='tweetengine',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
)
