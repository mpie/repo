# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser
#from resources.lib.modules import log_utils

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['watchserieshd.io']
        self.base_link = 'https://www4.watchserieshd.io'
        self.search_link = 'search.html?keyword=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query(title)))
            result = client.request(url)
            match = re.compile('<div class="video-thumbimg">.+?href="(.+?)".+?title="(.+?)"', re.DOTALL).findall(result)
            for url, name in match:
                    result = client.request(self.base_link + url)
                    final_page_match = re.compile('<div class="vc_col-sm-8 wpb_column column_container">.+?Released:(.+?)<.+?/series/(.+?)"', re.DOTALL).findall(result)
                    for release_year, fin_url in final_page_match:
                        release_year = release_year.replace(' ', '')
                        url = self.base_link + '/series/' + fin_url
                        if release_year == year:
                            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query(tvshowtitle)))
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            result = client.request(url)
            match = re.compile('<div class="video-thumbimg">.+?href="(.+?)".+?title="(.+?)"', re.DOTALL).findall(result)
            for url, name in match:
                result = client.request(self.base_link + url + '/season')
                episodes = re.findall('<div class="video_container">.+?<a href="(.+?)" class="view_more"></a></div>.+?class="videoHname"><b>(.+?)</b></a></span>.+?<div class="video_date icon-calendar">.+?, (.+?)</div>', result, re.DOTALL)
                for url2, ep_no, aired_year in episodes:
                    url = self.base_link + url2
                    ep_no = ep_no.replace('Episode ', '').replace(':', '')
                    if ep_no == episode:
                        return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            result = client.request(url)
            match = re.compile('href="#".+?data-video="(.+?)".+?class=".+?">(.+?)<', re.DOTALL).findall(result)
            for url, source_name in match:
                if 'm1' in source_name:
                    source_name = 'Gvideo'
                if 'vidnode' in url:
                    url = 'http:' + url
                    html2 = client.request(url)
                    single = re.findall("file: '(.+?)'.+?label: '(.+?)'", html2)
                    for playlink, quality in single:
                        quality = quality.replace(' ', '').lower()
                        if quality.lower() == 'auto':
                            if 'm22' in quality:
                                quality = '720p'
                            elif 'm37' in quality:
                                quality = '1080p'
                            else:
                                quality = 'SD'

                        sources.append({'source': source_name, 'quality': quality, 'language': 'en', 'url': playlink, 'direct': False, 'debridonly': False})
                else:
                    sources.append({'source': source_name, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url
