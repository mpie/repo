# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''

import re, urllib, urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.base_link = 'https://flenix.tv'
        self.search_link = '/engine/ajax/search.php'
        self.movie_link = '/engine/ajax/get.php'
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

            query = urlparse.urljoin(self.base_link, self.search_link)
            headers = {'Host': 'flenix.tv', 'Origin': self.base_link, 'Referer': self.base_link + '/', 'User-Agent': self.User_Agent}
            post = {'query': cleantitle.query(title)}
            c = client.request(self.base_link, output='cookie')
            result = client.request(query, XHR=True, post=post, headers=headers, cookie=c)

            match = re.compile('<a href="(.+?)" class="searchresult">.+?<span class="searchheading">(.+?)</span><span class="syear">').findall(result)
            for url, name in match:
                if cleantitle.getsearch(title).lower() in cleantitle.getsearch(name).lower():
                    id = re.compile('.+\/(\d+)-.+').findall(url)[0]
                    query = urlparse.urljoin(self.base_link, self.movie_link)
                    post = {'id': id, 'device': 'desktop'}

                    phpsessid = re.compile('.+PHPSESSID=(.+)?').findall(c)[0]
                    cookie = 'PHPSESSID=' + phpsessid + '; uppodhtml5_volume=1; _gat=1'
                    print cookie
                    headers = {'Host': 'flenix.tv', 'Origin': self.base_link, 'Referer': url, 'User-Agent': self.User_Agent}

                    # The first request is really important
                    client.request(url, headers=headers, cookie=cookie)
                    result = client.request(query, XHR=True, post=post, headers=headers, cookie=cookie)

                    print result
                    movies = result.split(',')
                    print movies
                    for movie in movies:
                        if '1080%' in movie:
                            quality = '1080p'
                        elif '720%' in movie:
                            quality = '720p'
                        else:
                            quality = 'SD'

                        sources.append({'source': 'CDN', 'quality': quality, 'language': 'en', 'url': movie, 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url

