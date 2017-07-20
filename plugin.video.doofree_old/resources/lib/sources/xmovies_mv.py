# -*- coding: utf-8 -*-

import re,urllib,urlparse,json,time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import directstream

class source:
    def __init__(self):
        self.domains = ['xmovies8.tv', 'xmovies8.ru']
        self.base_link = 'http://xmovies8.tv'
        self.moviesearch_link = '/movie/%s-%s/'


    def get_movie(self, imdb, title, year):
        try:
            url = self.moviesearch_link % (cleantitle.geturl(title.replace('\'', '-')), year)
            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, limit='1')
            r = client.parseDOM(r, 'title')[0]
            if not '(%s)' % year in r: raise Exception()
            return url
        except:
            return


    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            url = path = re.sub('/watching.html$', '', url.strip('/'))
            url = referer = url + '/watching.html'

            p = client.request(url)
            p = re.findall("data\s*:\s*{\s*id:\s*(\d+),\s*episode_id:\s*(\d+),\s*link_id:\s*(\d+)", p)[0]
            p = urllib.urlencode({'id': p[0], 'episode_id': p[1], 'link_id': p[2], '_': int(time.time() * 1000)})

            headers = {
            'Accept-Formating': 'application/json, text/javascript',
            'Server': 'cloudflare-nginx',
            'Referer': referer}

            r = urlparse.urljoin(self.base_link, '/ajax/movie/load_episodes')
            r = client.request(r, post=p, headers=headers, XHR=True)
            r = re.findall("load_player\(\s*'([^']+)'\s*,\s*'?(\d+)\s*'?", r)
            r = [i for i in r if int(i[1]) >= 720]

            for u in r:
                try:
                    p = urllib.urlencode({'id': u[0], 'quality': u[1], '_': int(time.time() * 1000)})
                    u = urlparse.urljoin(self.base_link, '/ajax/movie/load_player_v2')

                    u = client.request(u, post=p, headers=headers, XHR=True)
                    u = json.loads(u)['playlist']
                    u = client.request(u, headers=headers, XHR=True)
                    u = json.loads(u)['playlist'][0]['sources']
                    u = [i['file'] for i in u if 'file' in i]

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'XMovies', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


