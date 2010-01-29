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

available_languages = []

for lang in os.listdir(basepath):
    langpath = os.path.join(basepath, lang, 'LC_MESSAGES')
    available_languages.append(lang)
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

def request_languages(request):
    """Parses the request and return language list.
    
    Stolen from Products.PloneLanguageTool, under GPL (c) Plone Foundation
    """

    browser_pref_langs = request.headers.get('HTTP_ACCEPT_LANGUAGE', '')
    browser_pref_langs = browser_pref_langs.split(',')

    i = 0
    langs = []
    length = len(browser_pref_langs)

    # Parse quality strings and build a tuple like
    # ((float(quality), lang), (float(quality), lang))
    # which is sorted afterwards
    # If no quality string is given then the list order
    # is used as quality indicator
    for lang in browser_pref_langs:
        lang = lang.strip().lower().replace('_', '-')
        if lang:
            l = lang.split(';', 2)
            quality = []

            if len(l) == 2:
                try:
                    q = l[1]
                    if q.startswith('q='):
                        q = q.split('=', 2)[1]
                        quality = float(q)
                except:
                    pass

            if quality == []:
                quality = float(length-i)

            language = l[0]
            if baselanguage in available_languages:
                langs.append((quality, baselanguage))
            else:
                baselanguage = language.split('-')[0]
                langs.append((quality, baselanguage))
            
            i = i + 1

    # Sort and reverse it
    langs.sort()
    langs.reverse()

    # Filter quality string
    langs = map(lambda x: x[1], langs)

    return langs



# not sure what this should be good for, keep it as comment for now        
#from zope.component.interface import provideInterface
#itdname = ITranslationDomain.__module__ + '.' + ITranslationDomain.getName()        
#provideInterface(itdname, ITranslationDomain)