# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdpopcorns.eu']
        self.base_link = 'https://hdpopcorns.eu'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
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

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year']

            search_id = cleantitle.getsearch(title.lower())
            query = urlparse.urljoin(self.base_link, self.search_link % (search_id.replace(' ','+')))
            result = client.request(query, timeout=3)

            match = re.compile('<a href="(.+?)" data-url.+?oldtitle="(.+?)".+?>').findall(result)
            print match

            for url, name in match:
                if cleantitle.getsearch(title).lower() == cleantitle.getsearch(name).lower():
                    # need an extra step for tvshows
                    if 'tvshowtitle' in data:
                        season = '%d' % int(data['season'])
                        episode = '%d' % int(data['episode'])
                        url = url[:-1]
                        url = url.replace('/series/', '/episode/')
                        url += '-season-%s-episode-%s/' % (season, episode)
                        print url

                    result = client.request(url)
                    url = re.compile('<iframe src="(.+?)"').findall(result)[0]

                    if 'openload' in url:
                        sources.append({'source': 'Openload', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

            print sources
            return sources
        except:
            return sources

    def resolve(self, url):
        return url



