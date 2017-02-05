# -*- coding: utf-8 -*-

import re,urllib,urlparse,json,base64,time

from resources.lib.libraries import client
from resources.lib.libraries import cleantitle
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['movieshd.tv', 'movieshd.is', 'movieshd.watch', 'flixanity.is', 'flixanity.me']
        self.base_link = 'http://flixanity.watch'


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


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

                imdb = data['imdb'] ; year = data['year']

                if 'tvshowtitle' in data:
                    url = '%s/tv-show/%s/season/%01d/episode/%01d' % (self.base_link, cleantitle.geturl(title), int(data['season']), int(data['episode']))
                else:
                    url = '%s/movie/%s' % (self.base_link, cleantitle.geturl(title))

                result = client.request(url, limit='5')

                if result == None and not 'tvshowtitle' in data:
                    url += '-%s' % year
                    result = client.request(url, limit='5')

                result = client.parseDOM(result, 'title')[0]

                if '%TITLE%' in result: raise Exception()

                r = client.request(url, output='extended')

                if not imdb in r[0]: raise Exception()

            else:
                url = urlparse.urljoin(self.base_link, url)

                r = client.request(url, output='extended')


            cookie = r[4] ; headers = r[3] ; result = r[0]

            try: auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except: auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)

            headers['Authorization'] = auth
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Cookie'] = cookie
            headers['Referer'] = url


            u = '/ajax/jne.php'
            u = urlparse.urljoin(self.base_link, u)

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)

            c = client.request(u, post=post, headers=headers, XHR=True, output='cookie', error=True)

            headers['Cookie'] = cookie + '; ' + c

            r = client.request(u, post=post, headers=headers, XHR=True)
            r = str(json.loads(r))
            r = re.findall('\'(http.+?)\'', r) + re.findall('\"(http.+?)\"', r)

            for i in r:
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'MoviesHD', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


