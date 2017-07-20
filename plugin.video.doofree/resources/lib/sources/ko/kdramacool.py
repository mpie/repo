# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 DooFree
'''

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['ko']
        self.domains = ['kdramacool.com']
        self.base_link = 'http://kdramacool.com'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                if 'tvshowtitle' in data:
                    url = '%s/eng-sub-%s-episode-%01d/' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['episode']))

                else:
                    url = '%s/eng-sub-%s-%01d/' % (self.base_link, cleantitle.geturl(data['title']), int(data['year']))


                url = client.request(url, timeout='10', output='geturl')
                if url == None: raise Exception()

            else:
                url = urlparse.urljoin(self.base_link, url)
                r = client.request(url, timeout='10')

            r = client.request(url, timeout='10')
            r = client.parseDOM(r, 'iframe', ret='src')

            for i in r:
                if 'ads' in i:
                    pass
                           
                else:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(i.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')
                    sources.append({'source': host, 'quality': 'SD', 'language': 'ko', 'url': i, 'direct': False, 'debridonly': False})


            return sources
        except:
            return sources


    def resolve(self, url):
            return url


