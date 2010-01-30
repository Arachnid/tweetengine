""" load the message catalogs and provide them as ztk utilities."""
import os
from zope.interface import implements
from zope.component import getSiteManager
from zope.i18n.interfaces import (
    ITranslationDomain,
    INegotiator,
)
from zope.i18n import interpolate
from zope.i18n import translate
from zope.i18n import MessageFactory
from zope.i18n.translationdomain import TranslationDomain
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18nmessageid import Message
from chameleon.zpt import template
from chameleon.zpt.loader import TemplateLoader
from google.appengine.ext.webapp import Request

_ = MessageFactory('tweetengine')

basepath = os.path.join(os.path.dirname(__file__), 'locales')
gsm = getSiteManager()

available_languages = []

for lang in os.listdir(basepath):
    if lang.endswith('.pot'):
        continue
    langpath = os.path.join(basepath, lang, 'LC_MESSAGES')
    available_languages.append(lang)
    for file in os.listdir(langpath):
        domainpath = os.path.abspath(os.path.join(langpath, file))
        if not file.endswith('.mo'):
            continue
        domainname = file[:-3]
        domain = gsm.queryUtility(ITranslationDomain, domainname)
        if domain is None:
            domain = TranslationDomain(domainname)
            gsm.registerUtility(domain, ITranslationDomain, name=domainname)        
        domain.addCatalog(GettextMessageCatalog(lang, domainname, domainpath))

# negotiation sucks :( because Chameleon never passes a context into the 
# translate method of the template. but the target_language is passed.
# so we need to set the target language to what comes with the request as 
# 'Accept-Language' header. The RequestNegotiator then get this header value

class RequestNegotiator(object):
    
    implements(INegotiator)
    
    def getLanguage(self, available_languages, accept_languages_header):
        if isinstance(accept_languages_header, Request):
             accept_languages_header = accept_languages_header.headers.get('Accept-Language', '')
        accept_languages = self.accept_languages(accept_languages_header)
        for accepted_language in accept_languages:
            if accepted_language in available_languages:
                return accepted_language

    def accept_languages(self, browser_pref_langs):
        """Parses the request and return language list.
        
        browser_pref_langs is the plain Accept-Language http request header 
        value.
        
        Stolen from Products.PloneLanguageTool, under GPL (c) Plone Foundation,
        slightly modified.
        """
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
                langs.append((quality, language))
                if '-' in language:
                    baselanguage = language.split('-')[0]
                    langs.append((quality-0.001, baselanguage))
                i = i + 1
    
        # Sort and reverse it
        langs.sort()
        langs.reverse()
        
        # Filter quality string
        langs = map(lambda x: x[1], langs)
        return langs

negotiator =  RequestNegotiator()
gsm.registerUtility(negotiator, INegotiator)      

# we need a smarter translation method than Chameleon default
# maybe its slower, but we can introduce caching later

def smart_translate(msgid, domain=None, mapping=None, context=None,
                   target_language=None, default=None):
    """ target_language is expected to be the http accept-language header
    """
    if msgid is None:
        return

    if target_language is not None:
        return translate(
            msgid, domain=domain, mapping=mapping, context=target_language,
            target_language=None, default=default)

    if isinstance(msgid, Message):
        default = msgid.default
        mapping = msgid.mapping

    if default is None:
        default = unicode(msgid)

    if not isinstance(default, basestring):
        return default

    return interpolate(default, mapping)

class SmartI18nPageTemplateFile(template.PageTemplateFile):    
    translate = staticmethod(smart_translate)

class SmartI18nPageTextTemplateFile(template.PageTextTemplateFile):    
    translate = staticmethod(smart_translate)

TemplateLoader.formats = { 
    "xml"  : SmartI18nPageTemplateFile,
    "text" : SmartI18nPageTextTemplateFile,
}