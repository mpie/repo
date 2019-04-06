# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''

import re, urllib, urlparse, json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import jsunpack


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.base_link = 'https://gomostream.com/'
        self.gomo_link = 'https://gomostream.com/decoding_v3.php'
        self.tvshow_search_link = 'show/%s/%s-%s?src=mirror1'
        self.movie_search_link = 'movie/%s?src=mirror1'
        self.User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            print url
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            if 'tvshowtitle' in data:
                season = '%02d' % int(data['season'])
                episode = '%02d' % int(data['episode'])
                title = data['tvshowtitle']
                query = urlparse.urljoin(self.base_link, self.tvshow_search_link % (cleantitle.geturl(title), season, episode))
            else:
                title = data['title']
                query = urlparse.urljoin(self.base_link, self.movie_search_link % cleantitle.geturl(title))

            result = client.request(query)

            tc = re.compile('tc = \'(.+?)\';').findall(result)[0]

            if (tc):
                token = re.compile('"_token": "(.+?)",').findall(result)[0]

                post = {'tokenCode': tc, '_token': token}
                headers = {'Host': 'gomostream.com', 'Referer': query, 'User-Agent': self.User_Agent, 'x-token': self.tsd(tc)}
                result = client.request(self.gomo_link, XHR=True, post=post, headers=headers)

                urls = json.loads(result)
                for url in urls:
                    if 'gomostream' in url:
                        sources.append({'source': 'CDN', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        print url
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            result = client.request(url)

            for x in re.findall('(eval\s*\(function.*?)</script>', result, re.DOTALL):
                try:
                    result += jsunpack.unpack(x).replace('\\', '')
                except:
                    pass

            result = jsunpack.unpack(result)
            result = unicode(result, 'utf-8')
            links = [(match[0], match[1]) for match in re.findall('''['"]?file['"]?\s*:\s*['"]([^'"]+)['"][^}]*['"]?label['"]?\s*:\s*['"]([^'"]*)''', result, re.DOTALL)]
            print links
            if len(links):
                return links[0][0]
            else:
                match = re.compile(',"(.+?).mp4"').findall(result)
                return match[0] + '.mp4'

    def tsd(self, tokenCode):
        _13x48X = tokenCode
        _71Wxx199 = _13x48X[4:18][::-1]
        return _71Wxx199 + "18" + "432782"

