# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''

import re, urllib, urlparse, json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.base_link = 'https://gomostream.com/'
        self.gomo_link = 'https://gomostream.com/decoding_v3.php'
        self.search_link = 'movie/%s?src=mirror1'
        self.User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            query = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(title))
            result = client.request(query)

            tc = re.compile('tc = \'(.+?)\';').findall(result)[0]

            if (tc):
                token = re.compile('"_token": "(.+?)",').findall(result)[0]

                post = {'tokenCode': tc, '_token': token}
                headers = {'Host': 'gomostream.com', 'Referer': 'https://gomostream.com/movie/' + cleantitle.geturl(title) + '?src=mirror1', 'User-Agent': self.User_Agent, 'x-token': self.tsd(tc)}
                result = client.request(self.gomo_link, XHR=True, post=post, headers=headers)

                urls = json.loads(result)
                for url in urls:
                    if 'gomostream' in url:
                        sources.append({'source': 'CDN', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url

    def tsd(self, tokenCode):
        _13x48X = tokenCode
        _71Wxx199 = _13x48X[4:18][::-1]
        return _71Wxx199 + "18" + "432782"

