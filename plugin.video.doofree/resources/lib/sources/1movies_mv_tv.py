# -*- coding: utf-8 -*-


import re,urllib,urlparse,json,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.domains = ['1movies.tv']
        self.base_link = 'https://1movies.tv'
        self.search_link = '/movies/search?s=%s'

    def getOriginalTitle(self, imdb):
        try:
            tmdb_link = base64.b64decode(
                'aHR0cHM6Ly9hcGkudGhlbW92aWVkYi5vcmcvMy9maW5kLyVzP2FwaV9rZXk9MTBiYWIxZWZmNzZkM2NlM2EyMzQ5ZWIxMDQ4OTRhNmEmbGFuZ3VhZ2U9ZW4tVVMmZXh0ZXJuYWxfc291cmNlPWltZGJfaWQ=')
            t = client.request(tmdb_link % imdb, timeout='10')
            try: title = json.loads(t)['movie_results'][0]['original_title']
            except: pass
            try: title = json.loads(t)['tv_results'][0]['original_name']
            except: pass
            title = cleantitle.normalize(title)
            return title
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            url = self.searchMovie(title, year)

            if url == None:
                t = cache.get(self.getOriginalTitle, 900, imdb)
                if t != title:
                    url = self.searchMovie(t, year)

            return urllib.urlencode({'url': url, 'episode': 0})
        except:
            return

    def searchMovie(self, title, year):
        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.search_link % (cleantitle.geturl(title.replace('\'', '-'))))
            r = client.request(url, timeout='10')
            t = cleantitle.get(title)
            r = client.parseDOM(r, 'h2', attrs={'class': 'tit'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]
            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            return url.encode('utf-8')
        except:
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, year):
        try:
            title = cleantitle.normalize(title)
            t = cleantitle.get(title)

            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query('%s Season %01d' % (title.replace('\'', '-'), int(season)))))
            r = client.request(url, timeout='10')
            r = client.parseDOM(r, 'h2', attrs={'class': 'tit'})
            if r:
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
                r = [(i[0], re.findall('(.+?)\s+-\s+Season\s+(\d+)', i[1])) for i in r]
                r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
                r = [i[0] for i in r if t == cleantitle.get(i[1]) and int(season) == int(i[2])][0]
            else:
                url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query('%s %01d' % (title.replace('\'', '-'), int(year)))))
                r = client.request(url, timeout='10')
                r = client.parseDOM(r, 'h2', attrs={'class': 'tit'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
                r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
                r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
                r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            return url.encode('utf-8')
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            season = '%01d' % int(season)
            episode = '%01d' % int(episode)

            if 'tvshowtitle' in data:
                r = self.searchShow(data['tvshowtitle'], season, data['year'])

            if r == None:
                t = cache.get(self.getOriginalTitle, 900, imdb)
                if t != data['tvshowtitle']:
                    r = self.searchShow(t, season, data['year'])

            return urllib.urlencode({'url': r, 'episode': episode})
        except:
            return

    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = data['url']
            episode = int(data['episode'])

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            p = client.request(url, timeout='10')

            if episode > 0:
                r = client.parseDOM(p, 'div', attrs={'class': 'ep_link.+?'})[0]
                r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a'))
                r = [(i[0], re.findall('Episode\s+(\d+)', i[1])) for i in r]
                r = [(i[0], i[1][0]) for i in r]
                r = [i[0] for i in r if int(i[1]) == episode][0]
                p = client.request(r, timeout='10')

            p = re.findall('load_player\((\d+)\)', p)
            p = urllib.urlencode({'id': p[0]})
            headers = {'Referer': url}
            r = urlparse.urljoin(self.base_link, '/ajax/movie/load_player_v3')
            r = client.request(r, post=p, headers=headers, XHR=True, timeout='10')
            url = json.loads(r)['value']
            url = client.request(url, headers=headers, XHR=True, output='geturl', timeout='10')

            if 'openload.io' in url or 'openload.co' in url or 'oload.tv' in url:
                sources.append({'source': 'openload.co', 'quality': 'HD', 'provider': '1movies', 'url': url, 'direct': False,'debridonly': False})
                raise Exception()

            r = client.request(url, headers=headers, XHR=True, timeout='10')
            try:
                src = json.loads(r)['playlist'][0]['sources']
                links = [i['file'] for i in src if 'file' in i]
                for i in links:
                    try:
                        sources.append(
                            {'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': '1movies',
                             'url': i, 'direct': True, 'debridonly': False})
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


