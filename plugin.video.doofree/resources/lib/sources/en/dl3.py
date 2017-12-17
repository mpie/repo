# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''

import re, urllib, urlparse

from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.base_link = 'http://dl3.melimedia.net/mersad/serial/'

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
            headers = {}

            url = self.base_link

            contents = client.request(url, headers=headers, timeout='3')

            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(contents)
            for url, name in match:
                if name[0] == ' ':
                    name = name[1:]
                name = name.replace('/', '')
                url = self.base_link + url
                if title.lower().replace(' ', '') in name.lower().replace(' ', ''):
                    html = client.request(url, timeout=5)
                    match2 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
                    for url2, name2 in match2:
                        season = '%02d' % int(data['season'])

                        if 's' + season in url2:
                            url2 = url + url2
                            html2 = client.request(url2, timeout=5)
                            match3 = re.compile('<a href="(.+?)">(.+?)</a>').findall(html2)
                            for url3, name3 in match3:
                                url3 = url2 + url3
                                episode = '%02d' % int(data['episode'])
                                if 'S' + season + 'E' + episode in url3:
                                    if '1080p' in url3:
                                        qual = '1080p'
                                    elif '720p' in url3:
                                        qual = '720p'
                                    elif '560p' in url3:
                                        qual = 'SD'
                                    elif '480p' in url3:
                                        qual = 'SD'
                                    else:
                                        qual = 'SD'

                                    sources.append({'source': 'CDN', 'quality': qual, 'language': 'en', 'url': url3, 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url

