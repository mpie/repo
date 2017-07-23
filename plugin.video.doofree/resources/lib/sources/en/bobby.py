# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 DooFree
'''

import re, urllib, urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['bobbyhd.com']
        self.base_link = 'http://webapp.bobbyhd.com'
        self.search_link = '/search.php?keyword=%s'
        self.player_link = '/player.php?alias=%s'

    def matchAlias(self, title, aliases):
        try:
            for alias in aliases:
                if cleantitle.get(title) == cleantitle.get(alias['title']):
                    return True
        except:
            return False

    def searchMovie(self, title, year, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            title = cleantitle.getsearch(title)
            query = self.search_link % ('%s+%s' % (urllib.quote_plus(title), year))
            query = urlparse.urljoin(self.base_link, query)
            r = client.request(query, timeout='15', headers=headers, mobile=True)
            match = re.compile('alias=(.+?)\'">(.+?)</a>').findall(r)
            match = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in match]
            match = [(i[0], i[1][0][0], i[1][0][1]) for i in match if len(i[1]) > 0]
            r = [(i[0],i[1]) for i in match if self.matchAlias(i[1], aliases) and year == i[2]][0]
            return r
        except:
            return

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69'}
            aliases.append({'country': 'us', 'title': title})
            r = self.searchMovie(title, year, aliases, headers)
            url = {'type': 'movie', 'id': r[0], 'episode': 0, 'headers': headers}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69'}
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'tvshowtitle': tvshowtitle, 'year': year, 'headers': headers, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            headers = eval(data['headers'])
            aliases = eval(data['aliases'])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.getsearch(title)
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            r = client.request(query, headers=headers, timeout='30', mobile=True)
            match = re.compile('alias=(.+?)\'">(.+?)</a>').findall(r)
            r = [(i[0], re.findall('(.+?)\s+-\s+Season\s+(\d+)', i[1])) for i in match]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if self.matchAlias(i[1], aliases) and int(season) == int(i[2])][0]
            url = {'type': 'tvshow', 'id': r, 'episode': episode, 'season': season, 'headers': headers}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            if data['id'] == None: return sources
            headers = eval(data['headers'])

            url = urlparse.urljoin(self.base_link, self.player_link % data['id'])

            r = client.request(url, headers=headers, timeout='30', mobile=True)

            if data['type'] == 'tvshow':
                match = re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)\..+?</a>').findall(r)
            else:
                match = re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)</a>').findall(r)

            for url, ep in match:
                try:
                    if data['type'] == 'tvshow':
                        if int(data['episode']) != int(ep):
                            raise Exception()
                    quality = directstream.googletag(url)[0]['quality']
                    sources.append({'source': 'gvideo', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        return directstream.googlepass(url)
