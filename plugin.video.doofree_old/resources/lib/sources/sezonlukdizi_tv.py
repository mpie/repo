# -*- coding: utf-8 -*-


import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['sezonlukdizi.net', 'sezonlukdizi.com']
        self.base_link = 'http://sezonlukdizi.net'
        self.search_link = '/js/dizi4.js'
        self.video_link = '/ajax/dataEmbed.asp'

    def getImdbTitle(self, imdb):
        try:
            t = 'http://www.omdbapi.com/?i=%s' % imdb
            t = client.request(t)
            t = json.loads(t)
            t = cleantitle.normalize(t['Title'])
            return t
        except:
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            list = cache.get(self.sezonlukdizi_tvcache, 120)
            url = [i[0] for i in list if cleantitle.query(tvshowtitle) == i[1]]

            if not url:
                t = cache.get(self.getImdbTitle, 900, imdb)
                url = [i[0] for i in list if cleantitle.query(t) == i[1]]

            url = urlparse.urljoin(self.base_link, url[0])
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def sezonlukdizi_tvcache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)

            result = client.request(url, redirect=False)

            if not result:
                r = client.request(self.base_link)
                r = client.parseDOM(r, 'script', attrs={'type':'text/javascript'}, ret='src')
                url = [s for s in r if '/js/dizi' in s][0]
                url = urlparse.urljoin(self.base_link, url)
                result = client.request(url)

            result = re.compile('{(.+?)}').findall(result)
            result = [(re.findall('u\s*:\s*(?:\'|\")(.+?)(?:\'|\")', i), re.findall('d\s*:\s*(?:\'|\")(.+?)(?:\',|\")', i)) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(re.compile('/diziler(/.+?)(?://|\.|$)').findall(i[0]), re.sub('&#\d*;','', i[1])) for i in result]
            result = [(i[0][0] + '/', cleantitle.query(i[1])) for i in result if len(i[0]) > 0]

            return result
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return

        url = '%s%01d-sezon-%01d-bolum.html' % (url.replace('.html', ''), int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            for i in range(3):
                result = client.request(url)
                if not result == None: break

            result = re.sub(r'[^\x00-\x7F]+', ' ', result)

            pages = client.parseDOM(result, 'div', attrs = {'class': 'menu'})
            pages = client.parseDOM(pages, 'div', ret='data-id')

            for page in pages:
                try:
                    url = urlparse.urljoin(self.base_link, self.video_link)
                    post = 'id=%s' % page

                    for i in range(3):
                        result = client.request(url, post=post)
                        if not result == None: break

                    url = client.parseDOM(result, 'iframe', ret='src')[0]

                    if 'openload.io' in url or 'openload.co' in url or 'oload.tv' in url:
                        sources.append({'source': 'openload.co', 'quality': 'HD', 'provider': 'Sezonlukdizi', 'url': url, 'direct': False, 'debridonly': False})

                    if not '.asp' in url: raise Exception()

                    for i in range(3):
                        result = client.request(url)
                        if not result == None: break

                    captions = re.search('kind\s*:\s*(?:\'|\")captions(?:\'|\")', result)
                    if not captions: raise Exception()

                    links = re.findall('"?file"?\s*:\s*"([^"]+)"', result)

                    for url in links:
                        try:
                            if not url.startswith('http'):
                                url = client.request(url, output='geturl')
                            url = url.replace('\\', '')
                            url = directstream.googletag(url)[0]
                            sources.append({'source': 'gvideo', 'quality': url['quality'], 'provider': 'Sezonlukdizi', 'url': url['url'], 'direct': True, 'debridonly': False})
                        except:
                            pass

                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            for i in range(3):
                u = directstream.googlepass(url)
                if not u == None: break
            return u
        except:
            return


