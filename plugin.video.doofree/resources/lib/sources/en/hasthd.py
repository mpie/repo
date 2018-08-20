# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''

import re, urllib, urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        # self.base_link = 'http://dl.hastidl.me/remotes/'
        self.base_link = 'http://79.127.126.110/Film/1900-2016/'
        self.base_link_2 = 'http://79.127.126.110/Film/2016/'

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

    def searchShow(self, title, season, episode, aliases, headers):
        return self.base_link

    def searchMovie(self, title, year, aliases, headers):
        return self.base_link

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            aliases = eval(data['aliases'])
            headers = {}

            if 'tvshowtitle' in data:
                url = self.searchShow(title, int(data['season']), int(data['episode']), aliases, headers)
            else:
                url = self.searchMovie(title, data['year'], aliases, headers)

            contents = client.request(url, headers=headers, timeout='3')

            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(contents)
            for url,name in match:
                new_title = name.split('20')[0]
                if cleantitle.get(title).lower() in cleantitle.get(new_title).lower():
                    if 'tvshowtitle' in data:
                        season = '%02d' % int(data['season'])
                        episode = '%02d' % int(data['episode'])

                        episode_chk = 's%se%s' % (season, episode)
                        if episode_chk.lower() in url.lower():
                            if '1080p' in url:
                                qual = '1080p'
                            elif '720p' in url:
                                qual = '720p'
                            elif '560p' in url:
                                qual = '560p'
                            elif '480p' in url:
                                qual = 'SD'
                            else:
                                qual = 'SD'
                            url = self.base_link + url
                            sources.append({'source': 'CDN', 'quality': qual, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                    else:
                        if data['year'] in url:
                            if '3D' in url:
                                qual = '3D'
                            elif '1080p' in url:
                                qual = '1080p'
                            elif '720p' in url:
                                qual = '720p'
                            elif '480p' in url:
                                qual = 'SD'
                            else:
                                qual = 'SD'

                            url = self.base_link + url
                            sources.append({'source': 'CDN', 'quality': qual, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

            # 2016 folder
            url = self.base_link_2

            contents = client.request(url, headers=headers, timeout='3')

            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(contents)
            for url,name in match:
                new_title = name.split('20')[0]
                if cleantitle.get(title).lower() in cleantitle.get(new_title).lower():
                    if data['year'] in url:
                        if '3D' in url:
                            qual = '3D'
                        elif '1080p' in url:
                            qual = '1080p'
                        elif '720p' in url:
                            qual = '720p'
                        elif '480p' in url:
                            qual = 'SD'
                        else:
                            qual = 'SD'

                        url = self.base_link_2 + url
                        sources.append({'source': 'CDN', 'quality': qual, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url

