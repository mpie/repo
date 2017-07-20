# -*- coding: utf-8 -*-

import re,urllib

from resources.lib.libraries import client
from resources.lib.libraries import cloudflare
from resources.lib import resolvers

class source:
    def __init__(self):
        self.base_link = 'http://seriestv.us'
        self.search_link = '/?s=%s'

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = tvshowtitle
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return
            url = '%s Season %01d Episode %01d Watch Online' % (url, int(season), int(episode))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            query = url.replace('\'', '')
            query = query.replace('Marvels ', '').replace('E.L.D.', 'E.L.D')
            query = re.sub('\s+',' ',query)
            query = self.base_link + self.search_link % urllib.quote_plus('"'+query+'"')

            result = cloudflare.source(query)
            amount = client.parseDOM(result, 'h1', attrs = {'class': 'border-radius-5'})

            if '1 video' not in amount[0]:
                query = query.replace('Watch+Online', 'Full')
                result = cloudflare.source(query)
                amount = client.parseDOM(result, 'h1', attrs = {'class': 'border-radius-5'})

            if '1 video' in amount[0]:
                item = client.parseDOM(result, 'li', attrs = {'class': 'border-radius-5 box-shadow'})
                url = client.parseDOM(item, 'a', ret='href')[0]

                try:
                    result = cloudflare.source(url)

                    iframeUrl = client.parseDOM(result, 'iframe', ret='src')[0]
                    headers = {'Referer': url}
                    result = client.source(iframeUrl, headers=headers)

                    for match in re.compile('"file"\s*:\s*"([^"]+)"\s*,\s*"label"\s*:\s*"([^"]+)').findall(result):
                        if match[1] == '720p':
                            quality = 'HD'
                        else:
                            quality = 'SD'
                        sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'SeriesTV', 'url': match[0].replace(' ','')})
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
