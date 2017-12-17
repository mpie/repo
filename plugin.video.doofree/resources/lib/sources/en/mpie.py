# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''

import re, urllib, urllib2, urlparse, json, base64, time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser2
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.base_link = 'https://www.google.com'

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
        SS = '%02d' % season
        EE = '%02d' % episode
        try:
            search_term = cleantitle.getsearch(title) + '+' + 'S' + SS + 'E' + EE
            url = self.base_link + '/search?q=index+of+' + search_term
            return url
        except:
            return

    def searchMovie(self, title, year, aliases, headers):
        try:
            theyear = '+' + year
            search_term = cleantitle.getsearch(title)
            url = self.base_link + '/search?q=index+of+' + search_term + theyear
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
            aliases = eval(data['aliases'])
            headers = {}

            if 'tvshowtitle' in data:
                url = self.searchShow(title, int(data['season']), int(data['episode']), aliases, headers)
            else:
                url = self.searchMovie(title, data['year'], aliases, headers)

            contents = client.request(url, headers=headers, timeout='3')

            items = dom_parser2.parse_dom(contents, 'h3', attrs={'class': 'r'})
            items = [dom_parser2.parse_dom(i.content, 'a', req=['href']) for i in items]
            items = [(i[0].content, i[0].attrs['href']) for i in items]

            for item in items:
                NAME = item[0]
                movie_url = item[1]

                movie_url = movie_url.replace('%2520', '%20')
                if 'index of /' in NAME.replace('<b>', '').replace('</b>', '').lower():
                    search_term = cleantitle.getsearch(title)
                    if 'tvshowtitle' in data:
                        if 'plex' not in movie_url:
                            try:
                                content = client.request(movie_url, headers=headers, timeout='10')
                            except:
                                pass
                    else:
                        try:
                            content = client.request(movie_url, headers=headers, timeout='10')
                        except:
                            pass

                    match = re.compile('href="(.+?)"').findall(content)
                    for URL in match:
                        if not 'http' in URL:
                            MOVIE = movie_url + URL
                            if MOVIE[-4] == '.':
                                if MOVIE.endswith('.mkv') or MOVIE.endswith('.mp4'):
                                    CLEANURL = URL.replace('%20', '.').lower()
                                    if search_term.replace(' ', '.').replace('+', '.') in CLEANURL.replace(' ',
                                                                                                           '.').lower():
                                        if 'tvshowtitle' in data:
                                            SS = '%02d' % int(data['season'])
                                            EE = '%02d' % int(data['episode'])
                                            if 's' + SS in CLEANURL.replace(' ', ''):
                                                if 'e' + EE in CLEANURL.replace(' ', ''):
                                                    if '1080p' in MOVIE:
                                                        qual = '1080p'
                                                    elif '720p' in MOVIE:
                                                        qual = '720p'
                                                    elif '480p' in MOVIE:
                                                        qual = 'SD'
                                                    else:
                                                        qual = 'SD'

                                                    if '.mkv' in MOVIE or '.mp4' in MOVIE:
                                                        sources.append(
                                                            {'source': 'CDN', 'quality': qual, 'language': 'en',
                                                             'url': MOVIE, 'direct': True, 'debridonly': False})
                                        else:
                                            if data['year'] in MOVIE.lower():
                                                if '1080p' in MOVIE:
                                                    qual = '1080p'
                                                elif '720p' in MOVIE:
                                                    qual = '720p'
                                                elif '480p' in MOVIE:
                                                    qual = 'SD'
                                                else:
                                                    qual = 'SD'

                                                if '.mkv' in MOVIE or '.mp4' in MOVIE:
                                                    sources.append({'source': 'CDN', 'quality': qual, 'language': 'en',
                                                                    'url': MOVIE, 'direct': True, 'debridonly': False})

            # extra sources 1
            extra_url = 'http://dl.hastidl.net/remotes/'

            extra_contents = client.request(extra_url, headers=headers, timeout='3')

            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(extra_contents)

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
                                qual = 'SD'
                            elif '480p' in url:
                                qual = 'SD'
                            else:
                                qual = 'SD'
                            url = extra_url + url
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

            # extra sources 2
            extra_url2 = 'http://dl3.melimedia.net/mersad/serial/'

            extra_contents2 = client.request(extra_url2, headers=headers, timeout='3')

            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(extra_contents2)
            for url, name in match:
                if name[0] == ' ':
                    name = name[1:]
                name = name.replace('/', '')
                url = extra_url2 + url
                if title.lower().replace(' ', '') == name.lower().replace(' ', ''):
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

                                    sources.append({'source': 'CDN', 'quality': qual, 'language': 'en', 'url': url3,
                                                    'direct': True, 'debridonly': False})
            print sources
            return sources
        except:
            return sources

    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url

