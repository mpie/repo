# -*- coding: utf-8 -*-

import re,urllib,urlparse,random,subprocess,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client

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

            r = client.parseDOM(r, 'div', attrs = {'class': 'cell_container'})
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

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            post = urlparse.parse_qs(urlparse.urlparse(referer).query).values()[0][0]
            post = urllib.urlencode({'v': post})

            url = urlparse.urljoin(self.base_link, '/video_info/iframe')

            r = client.request(url, post=post, headers=headers, referer=referer)

            r = re.findall('"(\d+)"\s*:\s*"([^"]+)', r)
            r = [(urllib.unquote(i[1].split('url=')[-1]), i[0])  for i in r]

            links = [(i[0], '1080p') for i in r if int(i[1]) >= 1080]
            links += [(i[0], 'HD') for i in r if 720 <= int(i[1]) < 1080]
            links += [(i[0], 'SD') for i in r if 480 <= int(i[1]) < 720]

            for i in links: sources.append({'source': 'gvideo', 'quality': i[1], 'provider': 'Afdah', 'url': i[0], 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return
