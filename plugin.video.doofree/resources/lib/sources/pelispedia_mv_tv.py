# -*- coding: utf-8 -*-


import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['pelispedia.tv']
        self.base_link = 'http://www.pelispedia.tv'
        self.moviesearch_link = '/pelicula/%s/'
        self.tvsearch_link = '/serie/%s/'

    def get_movie(self, imdb, title, year):
        try:
            url = self.moviesearch_link % cleantitle.geturl(title)

            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, limit='1')
            r = client.parseDOM(r, 'title')

            if not r:
                url = 'http://www.imdb.com/title/%s' % imdb
                url = client.request(url, headers={'Accept-Language':'es-ES'})
                url = client.parseDOM(url, 'title')[0]
                url = re.sub('(?:\(|\s)\d{4}.+', '', url).strip()
                url = cleantitle.normalize(url.encode("utf-8"))
                url = self.moviesearch_link % cleantitle.geturl(url)

                r = urlparse.urljoin(self.base_link, url)
                r = client.request(r, limit='1')
                r = client.parseDOM(r, 'title')

            if not year in r[0]: raise Exception()

            return url
        except:
            pass

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = self.tvsearch_link % cleantitle.geturl(tvshowtitle)

            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, limit='1')
            r = client.parseDOM(r, 'title')

            if not r:
                url = 'http://www.imdb.com/title/%s' % imdb
                url = client.request(url, headers={'Accept-Language':'es-ES'})
                url = client.parseDOM(url, 'title')[0]
                url = re.sub('\((?:.+?|)\d{4}.+', '', url).strip()
                url = cleantitle.normalize(url.encode("utf-8"))
                url = self.tvsearch_link % cleantitle.geturl(url)

                r = urlparse.urljoin(self.base_link, url)
                r = client.request(r, limit='1')
                r = client.parseDOM(r, 'title')

            if not year in r[0]: raise Exception()

            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = '/pelicula/%s-season-%01d-episode-%01d/' % (url.strip('/').split('/')[-1], int(season), int(episode))
            return url
        except:
            return

    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            r = urlparse.urljoin(self.base_link, url)

            result = client.request(r)

            f = client.parseDOM(result, 'iframe', ret='src')
            f = [i for i in f if 'iframe' in i][0]

            result = client.request(f, headers={'Referer': r})

            r = client.parseDOM(result, 'div', attrs = {'id': 'botones'})[0]
            r = client.parseDOM(r, 'a', ret='href')
            r = [(i, urlparse.urlparse(i).netloc) for i in r]

            links = []

            for u, h in r:
                if not 'pelispedia' in h and not 'thevideos.tv' in h: continue

                result = client.request(u, headers={'Referer': f})

                try:
                    if 'pelispedia' in h: raise Exception()

                    url = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    url = re.findall('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')\s*,\s*label\s*:\s*(?:\"|\')(.+?)(?:\"|\')', url)
                    url = [i[0] for i in url if '720' in i[1]][0]

                    links.append({'source': 'cdn', 'quality': 'HD', 'url': url, 'direct': False})
                except:
                    pass

                try:
                    url = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    url = re.findall('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')', url)

                    for i in url:
                        try: links.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'url': i, 'direct': True})
                        except: pass
                except:
                    pass

                try:
                    post = re.findall('gkpluginsphp.*?link\s*:\s*"([^"]+)', result)[0]
                    post = urllib.urlencode({'link': post})

                    url = urlparse.urljoin(self.base_link, '/Pe_flsh/plugins/gkpluginsphp.php')
                    url = client.request(url, post=post, XHR=True, referer=u)
                    url = json.loads(url)['link']

                    links.append({'source': 'gvideo', 'quality': 'HD', 'url': url, 'direct': True})
                except:
                    pass

                try:
                    post = re.findall('var\s+parametros\s*=\s*"([^"]+)', result)[0]

                    post = urlparse.parse_qs(urlparse.urlparse(post).query)['pic'][0]
                    post = urllib.urlencode({'sou': 'pic', 'fv': '23', 'url': post})

                    url = urlparse.urljoin(self.base_link, '/Pe_Player_Html5/pk/pk_2/plugins/protected.php')
                    url = client.request(url, post=post, XHR=True)
                    url = json.loads(url)[0]['url']

                    links.append({'source': 'cdn', 'quality': 'HD', 'url': url, 'direct': True})
                except:
                    pass

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Pelispedia', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})
            print sources
            return sources
        except:
            return sources

    def resolve(self, url):
        return url


