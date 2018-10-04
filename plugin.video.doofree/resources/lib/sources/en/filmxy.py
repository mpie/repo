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
        self.domains = ['filmxy.me']
        self.base_link = 'https://www.filmxy.one/'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def filter_host(self, host):
        if host not in ['openload.co', 'yourupload.com', 'streamango.com', 'rapidvideo.com']:
            return False
        return True

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year']

            search_id = cleantitle.geturl(title.lower())
            query = urlparse.urljoin(self.base_link, self.search_link % (search_id.replace('-', '+')))
            # print query
            result = client.request(query)

            match = re.compile('class="single-post".+?href="(.+?)".+?<h2>(.+?)</h2>', re.DOTALL).findall(result)

            for mov_url, mov_tit in match:
                chk_tit = mov_tit.split('(')[0].strip()
                if cleantitle.getsearch(title).lower() == cleantitle.getsearch(chk_tit).lower():
                    if year in mov_tit:
                        result = client.request(mov_url)
                        streams = re.compile('data-player="&lt;iframe src=&quot;(.+?)&quot;', re.DOTALL).findall(result)

                        for link in streams:
                            host = link.split('//')[1].replace('www.', '')
                            host = host.split('/')[0].lower()
                            if not self.filter_host(host):
                                continue
                            sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url



