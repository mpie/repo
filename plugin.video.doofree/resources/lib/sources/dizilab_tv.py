# -*- coding: utf-8 -*-

import re,urllib,urlparse

from resources.lib.libraries import cleantitle
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://dizilab.com'
        self.search_link = '/arsiv?limit=&tur=&orderby=&ulke=&order=&yil=&dizi_adi=%s'

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.search_link % (urllib.quote_plus(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query)

            result = cloudflare.source(query)
            result = client.parseDOM(result, 'div', attrs = {'class': 'tv-series-single'})

            tvshowtitle = cleantitle.tv(tvshowtitle)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', {'class': 'title'}), re.compile('<span>\s*(\d{4})\s*</span>').findall(i)) for i in result]
            result = [(i[0][0], i[1][0], i[2][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            result = [(i[0], re.compile('([^>]+)$').findall(i[1]), i[2]) for i in result]
            result = [(i[0], i[1][0], i[2]) for i in result if len(i[1]) > 0]

            result = [i for i in result if tvshowtitle == cleantitle.tv(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = urlparse.urljoin(self.base_link, url)

            result = cloudflare.source(url)
            result = client.parseDOM(result, 'a', ret='href')
            result = [i for i in result if '/sezon-%01d/bolum-%01d' % (int(season), int(episode)) in i][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = cloudflare.source(url)

            links = re.compile('<a href="(.+?)?alternatif=(.+?)">').findall(result)
            url = links[-1][0] + 'alternatif=' + links[-1][1]

            result = cloudflare.source(url)
            iframe_link = re.compile('<iframe.+src="(.+).mp4"').findall(result)[0]

            try:
                sources.append({'source': 'openload', 'quality': 'HD', 'provider': 'Dizilab', 'url': iframe_link + '.mp4'})
            except:
                pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = resolvers.request(url)

            return url
        except:
            return

