# -*- coding: utf-8 -*-

import re,urllib,urlparse,json,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['tunemovies.to']
        self.base_link = 'https://tunemovies.to'
        self.search_link = '/search/%s.html'


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)
            query = query % urllib.quote_plus(title)

            t = cleantitle.get(title)

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs = {'class': 'thumb'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]

            url = [i[0] for i in r if t in cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = urlparse.urljoin(self.base_link, self.search_link)
            query = query % urllib.quote_plus(data['tvshowtitle'])

            t = cleantitle.get(data['tvshowtitle'])

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs = {'class': 'thumb'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]

            url = [i[0] for i in r if t in cleantitle.get(i[1]) and ('Season %s' % season) in i[1]][0]
            url += '?episode=%01d' % int(episode)

            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            try:
                url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except:
                episode = None

            ref = url

            for i in range(3):
                result = client.request(url)
                if not result == None: break

            if not episode == None:
                result = client.parseDOM(result, 'div', attrs = {'id': 'ip_episode'})[0]
                ep_url = client.parseDOM(result, 'a', attrs = {'data-name': str(episode)}, ret='href')[0]
                for i in range(3):
                    result = client.request(ep_url)
                    if not result == None: break

            r = client.parseDOM(result, 'div', attrs = {'class': '[^"]*server_line[^"]*'})

            for u in r:
                try:
                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/plugins/ipplugins.php')
                    p1 = client.parseDOM(u, 'a', ret='data-film')[0]
                    p2 = client.parseDOM(u, 'a', ret='data-server')[0]
                    p3 = client.parseDOM(u, 'a', ret='data-name')[0]
                    post = {'ipplugins': 1, 'ip_film': p1, 'ip_server': p2, 'ip_name': p3}
                    post = urllib.urlencode(post)
                    for i in range(3):
                        result = client.request(url, post=post, XHR=True, referer=ref, timeout='10')
                        if not result == None: break

                    result = json.loads(result)
                    u = result['s']
                    s = result['v']

                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/ipplayer/ipplayer.php')

                    post = {'u': u, 'w': '100%', 'h': '420', 's': s, 'n': 0}
                    post = urllib.urlencode(post)

                    for i in range(3):
                        result = client.request(url, post=post, XHR=True, referer=ref)
                        if not result == None: break

                    url = json.loads(result)['data']

                    if type(url) is list:
                        url = [i['files'] for i in url]
                        for i in url:
                            try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'TuneMovie', 'url': i, 'direct': True, 'debridonly': False})
                            except: pass

                    else:
                        url = client.request(url)
                        url = client.parseDOM(url, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
                        url += '|%s' % urllib.urlencode({'User-agent': client.randomagent()})
                        sources.append({'source': 'cdn', 'quality': 'HD', 'provider': 'TuneMovie', 'url': url, 'direct': False, 'debridonly': False})

                except:
                    pass

            return sources
        except:
            return sources


    def __resolve(self, result):
        try:
            result = client.parseDOM(result, 'div', attrs = {'id': 'player'})[0]

            try: url = client.parseDOM(result, 'iframe', ret='src')[0]
            except: pass
            try: url = base64.b64decode(re.compile('decode\("(.+?)"').findall(result)[0])
            except: pass

            if 'proxy.link=tunemovie' in url:
                url = re.compile('proxy[.]link=tunemovie[*]([^&]+)').findall(url)[-1]

                key = base64.b64decode('Q05WTmhPSjlXM1BmeFd0UEtiOGg=')
                decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key + (24 - len(key)) * '\0'))
                url = url.decode('hex')
                url = decrypter.feed(url) + decrypter.feed()

            url = resolvers.request(url)
            return url
        except:
            return


    def resolve(self, url):
        return directstream.googlepass(url)

