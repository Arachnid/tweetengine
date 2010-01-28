import os
import errno
import logging
import zipfile
from StringIO import StringIO

def _openInOrPlain(filename):
    try:
        fp = open(filename)
    except IOError, (code, msg):
        
        if code == errno.ENOENT:
            filename = filename + ".in"
            if os.path.exists(filename):
                fp = open(filename)        
        if code == 20:
            # we're in a zip file baby
            # first figure out, what the file is
            parts = filename.split('/')
            idx = len(parts)
            if idx < 2:
                raise
            while idx > 0:
                logging.info('PARTS: %s' % parts[0:idx])
                filepath = os.path.sep + os.path.join(*parts[0:idx])
                logging.info('CHECK: '+filepath)
                if os.path.isfile(filepath):
                    break
                idx -= 1
            logging.info('ABSOLUTE: '+filepath)
            relative_in_zip = os.path.join(*parts[idx:])
            logging.info('RELATIVE: '+relative_in_zip)
            zip = zipfile.ZipFile(filepath, 'r')
            # the next lines are just a zip.open in python 2.6
            fp = StringIO()
            fp.write(zip.read('zope/component/meta.zcml'))
            fp.name = parts[idx]
            fp.seek(0)
        else:
            raise        
    return fp

# patch :-(
import zope.configuration.xmlconfig
zope.configuration.xmlconfig.openInOrPlain = _openInOrPlain
