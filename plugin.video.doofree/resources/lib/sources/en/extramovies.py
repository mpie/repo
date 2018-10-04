# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import re, urllib, urlparse, base64
import requests

from resources.lib.modules import cleantitle
from resources.lib.modules import cfscrape

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['extramovies.trade']
        self.base_link = 'http://extramovies.trade'
        self.search_link = '/?s=%s'
        self.User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

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

    def filter_host(self, host):
        if host not in ['openload.co']:
            return False
        return True

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query(title)))
            headers = {'User-Agent': self.User_Agent}

            if 'tvshowtitle' in data:
                scraper = cfscrape.create_scraper()
                html = scraper.get(url, headers=headers).content

                match = re.compile('class="post-item.+?href="(.+?)" title="(.+?)"', re.DOTALL).findall(html)
                for url, item_name in match:
                    if cleantitle.getsearch(title).lower() in cleantitle.getsearch(item_name).lower():
                        season_url = '%02d' % int(data['season'])
                        episode_url = '%02d' % int(data['episode'])
                        sea_epi = 'S%sE%s' % (season_url, episode_url)

                        result = scraper.get(url, headers=headers, timeout=5).content
                        Regex = re.compile('href="(.+?)"', re.DOTALL).findall(result)
                        for ep_url in Regex:
                            if sea_epi in ep_url:
                                if '1080p' in ep_url:
                                    qual = '1080p'
                                elif '720p' in ep_url:
                                    qual = '720p'
                                elif '480p' in ep_url:
                                    qual = '480p'
                                else:
                                    qual = 'SD'

                                sources.append({'source': 'CDN', 'quality': qual, 'language': 'en', 'url': ep_url, 'direct': False, 'debridonly': True, 'debridonly': False})
            else:
                html = requests.get(url, headers=headers).content
                match = re.compile('<div class="thumbnail".+?href="(.+?)" title="(.+?)"', re.DOTALL).findall(html)

                for url, item_name in match:
                    if cleantitle.getsearch(title).lower() in cleantitle.getsearch(item_name).lower():
                        if '1080' in url:
                            quality = '1080p'
                        elif '720' in url:
                            quality = '720p'
                        else:
                            quality = 'SD'

                        result = requests.get(url, headers=headers, timeout=10).content
                        Regex = re.compile('href="/download.php.+?link=(.+?)"', re.DOTALL).findall(result)

                        for link in Regex:
                            if 'server=' not in link:
                                try:
                                    link = base64.b64decode(link)
                                except:
                                    pass
                                try:
                                    host = link.split('//')[1].replace('www.', '')
                                    host = host.split('/')[0].lower()
                                except:
                                    pass
                                if not self.filter_host(host):
                                    continue
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url
