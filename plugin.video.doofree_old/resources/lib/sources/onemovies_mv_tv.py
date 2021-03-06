# -*- coding: utf-8 -*-

import re,urllib,urlparse,json,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import directstream
from resources.lib.libraries import jsunfuck
from resources.lib.libraries import cache


class source:
    def __init__(self):
        self.domains = ['123movies.to', '123movies.ru', '123movies.is', '123movies.gs', '123-movie.ru',
                        '123movies-proxy.ru', '123movies.moscow', '123movies.msk.ru', '123movies.msk.ru',
                        '123movies.unblckd.me', 'gomovies.to']
        self.base_link = 'https://gomovies.to'
        self.search_link = '/ajax/suggest_search'
        self.search_link_2 = '/movie/search/%s'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/movie_episodes/%s'
        self.embed_link = '/ajax/load_embed/'
        self.token_link = '/ajax/movie_token?eid=%s&mid=%s'
        self.sourcelink = '/ajax/movie_sources/%s?x=%s&y=%s'

    def getImdbTitle(self, imdb):
        try:
            t = 'http://www.omdbapi.com/?i=%s' % imdb
            t = client.request(t)
            t = json.loads(t)
            t = cleantitle.normalize(t['Title'])
            return t
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            if not url:
                t = cache.get(self.getImdbTitle, 900, imdb)
                url = [i[0] for i in list if cleantitle.query(t) == i[1]]
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            tvshowtitle = cleantitle.get(tvshowtitle)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            if not url:
                t = cache.get(self.getImdbTitle, 900, imdb)
                url = [i[0] for i in list if cleantitle.query(t) == i[1]]
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['date'], url['season'], url['episode'] = title, date, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, headers):
        try:
            title = cleantitle.normalize(title)
            u = urlparse.urljoin(self.base_link, self.search_link)
            p = urllib.urlencode({'keyword': ('%s - Season %s' % (title, season))})
            r = client.request(u, post=p, XHR=True)
            r = json.loads(r)['content']
            r = zip(client.parseDOM(r, 'a', ret='href', attrs={'class': 'ss-title'}), client.parseDOM(r, 'a', attrs={'class': 'ss-title'}))
            r = [(i[0], i[1], re.findall('(.*?)\s+-\s+Season\s+(\d)', i[1])) for i in r]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
            url = [i[0] for i in r if self.matchAlias(i[2][0], aliases) and i[2][1] == season][0]
            return url
        except:
            return

    def searchMovie(self, title, year, headers):
        try:
            title = cleantitle.normalize(title)
            u = urlparse.urljoin(self.base_link, self.search_link)
            p = urllib.urlencode({'keyword': title})
            r = client.request(u, post=p, XHR=True)
            r = json.loads(r)['content']
            r = zip(client.parseDOM(r, 'a', ret='href', attrs={'class': 'ss-title'}), client.parseDOM(r, 'a', attrs={'class': 'ss-title'}))
            url = [i[0] for i in r if self.matchAlias(i[1], aliases)][0]
            return url
        except:
            return

    def get_sources(self, url, hostDict, hostprDict, lowDict):
        try:
            sources = []
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            headers = {}

            if 'tvshowtitle' in data:
                episode = int(data['episode'])
                url = self.searchShow(data['tvshowtitle'], data['season'], headers)
            else:
                episode = 0
                url = self.searchMovie(data['title'], data['year'], headers)

            mid = re.findall('-(\d+)', url)[-1]

            try:
                headers = {'Referer': url}
                u = urlparse.urljoin(self.base_link, self.server_link % mid)
                r = client.request(u, headers=headers, XHR=True)
                r = json.loads(r)
                r = client.parseDOM(r['html'], 'div', attrs = {'class': 'les-content'})
                ids = client.parseDOM(r, 'a', ret='data-id')
                servers = client.parseDOM(r, 'a', ret='data-server')
                labels = client.parseDOM(r, 'a', ret='title')
                r = zip(ids, servers, labels)

                for eid in r:
                    try:
                        try:
                            ep = re.findall('episode.*?(\d+):.*?',eid[2].lower())[0]
                        except:
                            ep = 0
                        if (episode == 0) or (int(ep) == int(episode)):
                            url = urlparse.urljoin(self.base_link, self.token_link % (eid[0], mid))
                            script = client.request(url)

                            if '$_$' in script:
                                params = self.uncensored1(script)
                            elif script.startswith('[]') and script.endswith('()'):
                                params = self.uncensored2(script)
                            elif '_x=' in script:
                                x = re.search('''_x=['"]([^"']+)''', script).group(1)
                                y = re.search('''_y=['"]([^"']+)''', script).group(1)

                                params = {'x': x, 'y': y}
                            else:
                                raise Exception()
                            u = urlparse.urljoin(self.base_link, self.sourcelink % (eid[0], params['x'], params['y']))
                            r = client.request(u)
                            url = json.loads(r)['playlist'][0]['sources']
                            url = [i['file'] for i in url if 'file' in i]
                            url = [directstream.googletag(i) for i in url]
                            url = [i[0] for i in url if i]
                            for s in url:
                                sources.append({'source': 'gvideo', 'quality': s['quality'], 'provider': 'OneMovies',
                                                'url': s['url'], 'direct': True, 'debridonly': False})
                    except:
                        pass
            except:
                pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if self.embed_link in url:
                result = client.request(url, XHR=True)
                url = json.loads(result)['embed_url']
                return url

            try:
                if not url.startswith('http'):
                    url = 'http:' + url

                for i in range(3):
                    u = directstream.googlepass(url)
                    if not u == None: break

                return u
            except:
                return
        except:
            return

    def uncensored(a, b):
        x = '';
        i = 0
        for i, y in enumerate(a):
            z = b[i % len(b) - 1]
            y = int(ord(str(y)[0])) + int(ord(str(z)[0]))
            x += chr(y)
        x = base64.b64encode(x)
        return x

    def uncensored1(self, script):
        try:
            script = '(' + script.split("(_$$)) ('_');")[0].split("/* `$$` */")[-1].strip()
            script = script.replace('(__$)[$$$]', '\'"\'')
            script = script.replace('(__$)[_$]', '"\\\\"')
            script = script.replace('(o^_^o)', '3')
            script = script.replace('(c^_^o)', '0')
            script = script.replace('(_$$)', '1')
            script = script.replace('($$_)', '4')

            vGlobals = {"__builtins__": None, '__name__': __name__, 'str': str, 'Exception': Exception}
            vLocals = {'param': None}
            exec (CODE % script.replace('+', '|x|'), vGlobals, vLocals)
            data = vLocals['param'].decode('string_escape')
            x = re.search('''_x=['"]([^"']+)''', data).group(1)
            y = re.search('''_y=['"]([^"']+)''', data).group(1)
            return {'x': x, 'y': y}
        except:
            pass

    def uncensored2(self, script):
        try:
            js = jsunfuck.JSUnfuck(script).decode()
            x = re.search('''_x=['"]([^"']+)''', js).group(1)
            y = re.search('''_y=['"]([^"']+)''', js).group(1)
            return {'x': x, 'y': y}
        except:
            pass


