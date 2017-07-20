# -*- coding: utf-8 -*-

import re,urlparse

from resources.lib.libraries import client
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['rainierland.com']
        self.base_link = 'http://rainierland.com'
        self.movie_link = '/movie/%s-%s.html'


    def get_movie(self, imdb, title, year):
        try:
            url = re.sub('([^\s\-\w])+', '', title.lower()).replace(' ', '-')
            url = self.movie_link % (url, year)
            url = urlparse.urljoin(self.base_link, url)

            url = client.request(url, output='geturl')

            if url == None: raise Exception()

            url = urlparse.urljoin(self.base_link, url)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            r = client.parseDOM(r, 'div', attrs = {'class': 'screen fluid-width-video-wrapper'})[0]
            r = re.findall('src\s*=\s*"(.*?)"', r)[0]

            r = urlparse.urljoin(self.base_link, r)

            r = client.request(r, referer=url)

            links = []

            url = re.findall('src\s*=\s*"(.*?)"', r)
            url = [i for i in url if 'http' in i]

            for i in url:
                try: links += [{'source': 'gvideo', 'url': i, 'quality': directstream.googletag(i)[0]['quality'], 'direct': True}]
                except: pass

            url = re.findall('(openload\.(?:io|co)/(?:embed|f)/[0-9a-zA-Z-_]+)', r)
            url = ['http://' + i for i in url]

            for i in url:
                try: links += [{'source': 'openload.co', 'url': i, 'quality': 'HD', 'direct': False}]
                except: pass

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Rainierland', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


