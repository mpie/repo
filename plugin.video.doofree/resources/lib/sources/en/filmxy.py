# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2019 Mpie
'''

import urllib, urlparse, re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['filmxy.me']
        self.base_link = 'https://www.filmxy.live/'
        self.search_link = 'search/%s/feed/rss2/'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None: return
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            title = data['title']
            year = data['year']

            tit = cleantitle.geturl(title + ' ' + year)
            query = urlparse.urljoin(self.base_link, tit)

            r = self.scraper.get(query, params={'referer': self.base_link}).content
            if not data['imdb'] in r:
                return sources

            links = []

            try:
                down = client.parseDOM(r, 'div', attrs={'id': 'tab-download'})[0]
                down = client.parseDOM(down, 'a', ret='href')[0]
                data = client.request(down)
                frames = client.parseDOM(data, 'div', attrs={'class': 'single-link'})
                frames = [client.parseDOM(i, 'a', ret='href')[0] for i in frames if i]
                for i in frames:
                    links.append(i)

            except Exception:
                pass
            try:
                streams = client.parseDOM(r, 'div', attrs={'id': 'tab-stream'})[0]
                streams = re.findall('''iframe src=(.+?) frameborder''', streams.replace('&quot;', ''),
                                     re.I | re.DOTALL)
                for i in streams:
                    links.append(i)
            except Exception:
                pass

            for url in links:
                try:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if not valid:
                        valid, host = source_utils.is_host_valid(url, hostprDict)
                        if not valid:
                            continue
                        else:
                            rd = True
                    else:
                        rd = False
                    quality, info = source_utils.get_release_quality(url, url)
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    if rd:
                        sources.append(
                            {'source': host, 'quality': quality, 'language': 'en', 'url': url,
                             'direct': False,
                             'debridonly': True})
                    else:
                        sources.append(
                            {'source': host, 'quality': quality, 'language': 'en', 'url': url,
                             'direct': False,
                             'debridonly': False})
                except Exception:
                    pass
            return sources
        except Exception:
            return sources

    def resolve(self, url):

        return url