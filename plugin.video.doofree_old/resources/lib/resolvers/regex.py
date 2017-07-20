# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client


def resolve(url):
    try:
        data = str(url).replace('\r','').replace('\n','').replace('\t','')
        doregex = re.compile('\$doregex\[(.+?)\]').findall(data)

        for i in range(0, 5):
            for x in doregex:
                try:
                    if not '$doregex[%s]' % x in data: raise Exception()

                    regex = re.compile('<regex>(.+?)</regex>').findall(data)
                    regex = [r for r in regex if '<name>%s</name>' % x in r][0]

                    if '$doregex' in regex: raise Exception()

                    expres = re.compile('<expres>(.+?)</expres>').findall(regex)[0]

                    try: referer = re.compile('<referer>(.+?)</referer>').findall(regex)[0]
                    except: referer = ''
                    referer = urllib.unquote_plus(referer)
                    referer = client.replaceHTMLCodes(referer)
                    referer = referer.encode('utf-8')

                    page = re.compile('<page>(.+?)</page>').findall(regex)[0]
                    page = urllib.unquote_plus(page)
                    page = client.replaceHTMLCodes(page)
                    page = page.encode('utf-8')

                    result = client.request(page, referer=referer)
                    result = str(result).replace('\r','').replace('\n','').replace('\t','')
                    result = str(result).replace('\/','/')

                    r = re.compile(expres).findall(result)[0]
                    data = data.replace('$doregex[%s]' % x, r)
                except:
                    pass

        url = re.compile('(.+?)<regex>').findall(data)[0]
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')

        if not '$doregex' in url: return url
    except:
        return

