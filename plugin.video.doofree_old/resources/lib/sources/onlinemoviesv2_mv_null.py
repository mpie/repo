# -*- coding: utf-8 -*-

import re,urllib,urlparse

from resources.lib.libraries import cleantitle
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://onlinemovies.is'
        self.search_link = '/?s=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            result = cloudflare.source(query)

            title = cleantitle.movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = client.parseDOM(result, 'li', attrs = {'class': 'border.+?'})
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(i[0], client.parseDOM(i[1], 'span')) for i in result]
            result = [(i[0], i[1][0]) for i in result if len(i[1]) > 0]
            result = [(i[0], re.compile('(.+)[\.|\(|\[|\s](\d{4})[\.|\)|\]|\s|]').findall(i[1])) for i in result]
            result = [(i[0], i[1][0][0].strip(), i[1][0][1]) for i in result if len(i[1]) > 0]
            result = [i for i in result if any(x in i[2] for x in years)]
            result = [i[0] for i in result if title == cleantitle.movie(i[1])][0]

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

            quality = re.compile('>Quality:(.+?)\n').findall(result)[0]

            if 'CAM' in quality or 'TS' in quality: quality = 'CAM'
            elif 'SCREENER' in quality: quality = 'SCR'
            else: quality = 'HD'

            try:
                url = client.parseDOM(result, 'iframe', ret='src')
                url = [i for i in url if 'videomega' in i.lower()][0]
                url = re.compile('[ref|hashkey]=([\w]+)').findall(url)
                url = 'http://videomega.tv/cdn.php?ref=%s' % url[0]
                url = resolvers.request(url)
                if url == None: raise Exception()
                sources.append({'source': 'Videomega', 'quality': quality, 'provider': 'Onlinemoviesv2', 'url': url})
            except:
                pass

            try:
                url = client.parseDOM(result, 'iframe', ret='src')
                url = [i for i in url if 'openload' in i.lower()][0]
                url = resolvers.request(url)
                if url == None: raise Exception()
                sources.append({'source': 'Openload', 'quality': quality, 'provider': 'Onlinemoviesv2', 'url': url})
            except:
                pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


