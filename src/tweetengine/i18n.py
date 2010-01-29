""" load the message catalogs and provide them as ztk utilities."""
import os
import logging
from zope.component import (
    queryUtility,
    provideUtility,
    getSiteManager,
)
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.translationdomain import TranslationDomain
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog

basepath = os.path.join(os.path.dirname(__file__), 'locales')
gsm = getSiteManager()

for lang in os.listdir(basepath):
    langpath = os.path.join(basepath, lang, 'LC_MESSAGES')
    for file in os.listdir(langpath):
        domainpath = os.path.abspath(os.path.join(langpath, file))
        if not file.endswith('.mo'):
            continue
        domainname = file[:-3]
        domain = queryUtility(ITranslationDomain, domainname)
        if domain is None:
            domain = TranslationDomain(domainname)
            gsm.registerUtility(domain, ITranslationDomain, name=domainname)        
        domain.addCatalog(GettextMessageCatalog(lang, domainname, domainpath))

# not sure what this should be good for, keep it as comment for now        
#from zope.component.interface import provideInterface
#itdname = ITranslationDomain.__module__ + '.' + ITranslationDomain.getName()        
#provideInterface(itdname, ITranslationDomain)