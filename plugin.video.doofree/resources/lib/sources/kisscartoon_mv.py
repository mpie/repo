# -*- coding: utf-8 -*-

import re,urllib,urlparse,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cloudflare

class source:
    def __init__(self):
        self.base_link = 'http://kisscartoon.me'
        self.search_link = '/Search/Cartoon'
        self.headers = {'Referer': 'http://kisscartoon.me/'}
        self.cookie = {}

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link
            query = urlparse.urljoin(self.base_link, query)

            if title == 'WALLAE':
                title = 'WALL·E'

            post = urllib.urlencode({'keyword': title})
            result = cloudflare.source(query, post=post)

            result = client.parseDOM(result, 'table', attrs = {'class': 'listing'})
            result = client.parseDOM(result, 'a', ret='href')

            title = cleantitle.movie(title)
            try: url = [i for i in result if title in cleantitle.movie(i)][0]
            except: pass

            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        sources = []

        if url == None: return sources

        orgUrl = url
        url = urlparse.urljoin(self.base_link, url)
        url = url.replace('·', '\xb7')

        result = cloudflare.source(url)

        if '?' not in url:
            url = client.parseDOM(result, 'a', attrs={'href':orgUrl+'/Movie.+?'}, ret='href')[0]
            url = urlparse.urljoin(self.base_link, url)
            result = cloudflare.source(url)

        items = client.parseDOM(result, 'select', attrs={'id':'selectQuality'})
        items = re.compile('"(.+?)".+?(\d+?)p').findall(items[0])

        for item in items:
            try:
                u = base64.b64decode(item[0])
                u = u.encode('utf-8')
                if item[1] not in ['720', '1080']:
                    quality = 'SD'
                else:
                    quality = 'HD'

                sources.append({'source': 'GVideo', 'quality': quality, 'provider': 'KissCartoon', 'url': u})
            except:
                pass
        print sources
        return sources

    def resolve(self, url):
        return url
