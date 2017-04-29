# -*- coding: utf-8 -*-


import re,urllib,urlparse,hashlib,random,string,time,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['watch5s.to', 'cmovieshd.com', 'pmovies.to', 'watch5s.is']
        self.base_link = 'https://pmovies.to'
        self.info_link = '/ajax/movie_qtip/%s'
        self.token_link = 'https://redirector-googlevideo.streamdor.co/token.php'
        self.grabber_link = 'https://redirector-googlevideo.streamdor.co/grabber-api-v2/episode/%s?hash=%s&token=%s&_=%s'
        self.backup_token_link = 'https://redirector-googlevideo.streamdor.co/embed/go?type=token&eid=%s&mid=%s&_=%s'
        self.backup_link = 'https://redirector-googlevideo.streamdor.co/embed/go?type=sources&eid=%s&x=%s&y=%s'

    def get_movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
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
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, date, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            if 'tvshowtitle' in data:
                url = '/tv-series/%s-season-%01d/watch/' % (cleantitle.geturl(title), int(data['season']))
                year = str((int(data['year']) + int(data['season'])) - 1)
                episode = '%01d' % int(data['episode'])

            else:
                url = '/movie/%s/watch/' % cleantitle.geturl(title)
                year = data['year']
                episode = None

            url = urlparse.urljoin(self.base_link, url)
            referer = url

            r = client.request(url)

            y = re.findall('Release\s*:\s*.+?\s*(\d{4})', r)[0]

            if not year == y: raise Exception()

            r = client.parseDOM(r, 'div', attrs = {'class': 'les-content'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a'))
            r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]

            if not episode == None:
                r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
            else:
                r = [i[0] for i in r]

            r = [i for i in r if 'server=' in i]

            for u in r:
                try:
                    p = client.request(u, referer=referer, timeout='10')

                    t = re.findall('player_type\s*:\s*"(.+?)"', p)[0]
                    if t == 'embed': raise Exception()

                    episodeId = re.findall('episode\s*:\s*"(.+?)"', p)[0]
                    r = client.request(self.token_link,post=urllib.urlencode({'id': episodeId}), referer=referer, timeout='10')
                    js = json.loads(r)
                    hash = js['hash']
                    token = js['token']
                    _ = js['_']
                    url = self.grabber_link % (episodeId, hash, token, _)
                    u = client.request(url, referer=referer, timeout='10')
                    js = json.loads(u)

                    try:
                        u = js['playlist'][0]['sources']
                        u = [i['file'] for i in u if 'file' in i]

                        for i in u:
                            try:
                                sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'],
                                                'provider': 'pmovies', 'url': i, 'direct': True, 'debridonly': False})
                            except:
                                pass
                    except:
                        pass

                    try:
                        u = js['backup']
                        u = urlparse.parse_qs(urlparse.urlsplit(u).query)
                        u = dict([(i, u[i][0]) if u[i] else (i, '') for i in u])
                        eid = u['eid']
                        mid = u['mid']
                        p = client.request(self.backup_token_link % (eid, mid, _), XHR=True, referer=referer, timeout='10')
                        x = re.search('''_x=['"]([^"']+)''', p).group(1)
                        y = re.search('''_y=['"]([^"']+)''', p).group(1)
                        u = client.request(self.backup_link % (eid, x, y), referer=referer, XHR=True, timeout='10')
                        js = json.loads(u)
                        try:
                            u = js['playlist'][0]['sources']
                            u = [i['file'] for i in u if 'file' in i]

                            for i in u:
                                try:
                                    sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'],
                                                    'provider': 'pmovies', 'url': i, 'direct': True, 'debridonly': False})
                                except:
                                    pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return directstream.googlepass(url)


