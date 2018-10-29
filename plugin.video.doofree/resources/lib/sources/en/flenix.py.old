# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''

import re, urllib, urlparse, json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.base_link = 'https://www2.flenix.cc/'
        self.gomo_link = 'https://gomostream.com/decoding_v3.php'
        self.search_link = 'search?s=%s'
        self.movie_link = '/engine/ajax/get.php'
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
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = title.replace('Marvel\'s ', '')

            query = urlparse.urljoin(self.base_link, self.search_link % cleantitle.getsearch(title))
            #print query
            result = client.request(query)
            match = re.compile('<a href="(.+?)" class="ml-mask jt" oldtitle="(.+?)".+?>').findall(result)
            #print match

            for url, name in match:
                if cleantitle.getsearch(title).lower() == cleantitle.getsearch(name).lower():
                    # need an extra step for tvshows
                    if 'tvshowtitle' in data:
                        season = '%02d' % int(data['season'])
                        seasonx = '%d' % int(data['season'])
                        episode = '%d' % int(data['episode'])
                        url += '?season=%s' % (season)

                        #print url
                        result = client.request(url)
                        match = re.compile('<a href="(.+?)" class="ml-mask jt" oldtitle="(.+?)".+?>').findall(result)
                        #print match
                        for episode_url, name in match:
                            episode_chk = '%sx%s/' % (season, episode)
                            episode_chkx = '%sx%s/' % (seasonx, episode)
                            if episode_chk.lower() in episode_url.lower() or episode_chkx.lower() in episode_url.lower():
                                #print episode_url
                                result = client.request(episode_url)
                                video = re.compile('<a href="(.+?)" title="(.+?)" class="thumb mvi-cover"').findall(result)[0]

                    else:
                        result = client.request(url)
                        video = re.compile('<a href="(.+?)" title="(.+?)" class="thumb mvi-cover"').findall(result)[0]

                    #print video
                    # video player
                    result = client.request(video[0])
                    iframe = re.compile('<iframe src="(.+?)"').findall(result)[0]

                    # get video src
                    result = client.request(iframe)
                    tc = re.compile('tc = \'(.+?)\';').findall(result)[0]
                    token = re.compile('"_token": "(.+?)",').findall(result)[0]

                    post = {'tokenCode': tc, '_token': token}
                    headers = {'Host': 'gomostream.com', 'Referer': 'https://gomostream.com/movie/' + cleantitle.geturl(title) + '?src=mirror1', 'User-Agent': self.User_Agent, 'x-token': self.tsd(tc)}
                    result = client.request(self.gomo_link, XHR=True, post=post, headers=headers)

                    urls = json.loads(result)
                    for url in urls:
                        if 'gomostream' in url:
                            sources.append({'source': 'CDN', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                        if 'streamango' in url:
                            sources.append({'source': 'Streamango', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                        if 'openload' in url:
                            url = url.replace('embed', 'f')
                            sources.append({'source': 'Openload', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})


            return sources
        except:
            return sources

    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url

    def tsd(self, tokenCode):
        _13x48X = tokenCode
        _71Wxx199 = _13x48X[4:18][::-1]
        return _71Wxx199 + "18" + "432782"

