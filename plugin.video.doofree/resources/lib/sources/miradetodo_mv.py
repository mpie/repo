# -*- coding: utf-8 -*-

import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['miradetodo.net']
        self.base_link = 'http://miradetodo.net'
        self.search_link = '/?s=%s'


    def get_movie(self, imdb, title, year):
        try:
            t = 'http://www.imdb.com/title/%s' % imdb
            t = client.request(t, headers={'Accept-Language':'ar-AR'})
            t = client.parseDOM(t, 'title')[0]
            t = re.sub('(?:\(|\s)\d{4}.+', '', t).strip()

            q = self.search_link % urllib.quote_plus(t)
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q)

            r = client.parseDOM(r, 'div', attrs = {'class': 'item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'class': 'tt'}), client.parseDOM(i, 'span', attrs = {'class': 'year'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [i[0] for i in r if cleantitle.get(t) == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass


    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            r = urlparse.urljoin(self.base_link, url)

            result = client.request(r)

            f = client.parseDOM(result, 'div', attrs = {'class': 'movieplay'})
            f = [re.findall('(?:\"|\')(http.+?miradetodo\..+?)(?:\"|\')', i) for i in f]
            f = [i[0] for i in f if len(i) > 0]


            dupes = []

            for u in f:
                try:
                    sid = urlparse.parse_qs(urlparse.urlparse(u).query)['id'][0]

                    if sid in dupes: raise Exception()
                    dupes.append(sid)

                    url = client.request(u, timeout='10', XHR=True, referer=u)
                    url = client.parseDOM(url, 'a', ret='href')
                    url = [i for i in url if '.php' in i][0]
                    url = 'http:' + url if url.startswith('//') else url
                    url = client.request(url, timeout='10', XHR=True, referer=u)

                    s = re.findall('file\s*:\s*"(.+?)"', url)
                    s += re.findall('"file"\s*:\s*"(.+?)"', url)
                    s = [x.replace('\\', '') for x in s]

                    for i in s:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Miradetodo', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


