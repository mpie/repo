# -*- coding: utf-8 -*-


import re,urllib,urlparse,json,base64,time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['putlocker.systems']
        self.base_link = 'http://www.putlocker.systems'


    def get_movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def get_tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, season, episode):
        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['season'], url['episode'] = title, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

                imdb = data['imdb']

                match = title.replace('-', '').replace(':', '').replace('\'', '').replace(' ', '-').replace('--', '-').lower()

                if 'tvshowtitle' in data:
                    url = '%s/show/%s/season/%01d/episode/%01d' % (self.base_link, match, int(data['season']), int(data['episode']))
                else:
                    url = '%s/movie/%s' % (self.base_link, match)

                result = client.request(url, limit='1')
                result = client.parseDOM(result, 'title')[0]

                if '%TITLE%' in result: raise Exception()

                result, headers, content, cookie = client.request(url, output='extended')

                if not imdb in result: raise Exception()


            else:

                result, headers, content, cookie = client.request(url, output='extended')


            auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            auth = 'Bearer %s' % urllib.unquote_plus(auth)

            headers['Authorization'] = auth
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Referer'] = url

            u = 'http://www.putlocker.systems/ajax/embeds.php'

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)


            r = client.request(u, post=post, headers=headers)
            r = str(json.loads(r))
            r = client.parseDOM(r, 'iframe', ret='.+?') + client.parseDOM(r, 'IFRAME', ret='.+?')

            links = []

            for i in r:
                try: links += [{'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'url': i, 'direct': True}]
                except: pass

            links += [{'source': 'openload.co', 'quality': 'SD', 'url': i, 'direct': False} for i in r if 'openload.co' in i]

            links += [{'source': 'videomega.tv', 'quality': 'SD', 'url': i, 'direct': False} for i in r if 'videomega.tv' in i]


            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Putlocker', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        print url
        return url


