# -*- coding: utf-8 -*-

import re,urllib,urlparse,random,subprocess,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import directstream

class source:
    def __init__(self):
        self.domains = ['fmovie.co', 'afdah.org', 'xmovies8.org', 'putlockerhd.co']
        self.base_link = 'https://fmovie.co'
        self.search_link = '/results?q=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs={'class': 'cell_container'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            referer = urlparse.urljoin(self.base_link, url)

            try:
                post = urlparse.parse_qs(urlparse.urlparse(referer).query).values()[0][0]
            except:
                post = referer.strip('/').split('/')[-1].split('watch_', 1)[-1].rsplit('#')[0].rsplit('.')[0]

            post = urllib.urlencode({'v': post})

            url = urlparse.urljoin(self.base_link, '/video_info/iframe')

            r = client.request(url, post=post, XHR=True, referer=url)
            r = json.loads(r).values()
            r = [urllib.unquote(i.split('url=')[-1]) for i in r]

            for i in r:
                try:
                    sources.append(
                        {'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Afdah',
                         'url': i, 'direct': True, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)
