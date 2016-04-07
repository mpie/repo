# -*- coding: utf-8 -*-

import re,urllib,urlparse

from resources.lib.libraries import client
from resources.lib.libraries import cloudflare
from resources.lib import resolvers

class source:
    def __init__(self):
        self.base_link = 'http://usmovieshd.com/'
        self.search_link = '/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            title = title.replace(':', '').replace(' - ', ' ')
            title = re.sub('\s+',' ',title)
            query = self.search_link % urllib.quote_plus(title + ' ' + year)
            query = urlparse.urljoin(self.base_link, query)

            result = cloudflare.source(query)
            amount = client.parseDOM(result, 'h1', attrs = {'class': 'border-radius-5'})

            if 'videos' not in amount[0]:
                query = query.replace('Watch+Online', 'Full')
                result = cloudflare.source(query)
                amount = client.parseDOM(result, 'h1', attrs = {'class': 'border-radius-5'})
            print query
            if 'videos' in amount[0]:
                item = client.parseDOM(result, 'li', attrs = {'class': 'border-radius-5 box-shadow'})
                url = client.parseDOM(item, 'a', ret='href')[0]

                return url
        except:
            pass

        return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            result = cloudflare.source(url)

            iframeUrl = client.parseDOM(result, 'iframe', ret='src')[0]
            headers = {'Referer': url}
            result = client.source(iframeUrl, headers=headers)

            for match in re.compile('"file"\s*:\s*"([^"]+)"\s*,\s*"label"\s*:\s*"([^"]+)').findall(result):
                if match[1] == '720p':
                    quality = 'HD'
                else:
                    quality = 'SD'
                sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'USMoviesHD', 'url': match[0].replace(' ','')})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return
