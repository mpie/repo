# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['dwatchseries.to']
        self.base_link = 'http://dwatchseries.to'
        self.search_link = '/search/%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query(tvshowtitle)))
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            headers = {'User_Agent': User_Agent, 'referer': self.base_link}
            result = client.request(url.lower().replace('+','%20'), headers=headers)

            link = result.split('Search results')[1:]
            links = re.findall(r'<a href="([^"]+)" title=".*?" target="_blank"><strong>([^<>]*)</strong></a>', str(link), re.I | re.DOTALL)

            for media_url, media_title in links:
                if not cleantitle.get(url.rsplit('/', 1)[-1]).lower().replace('+','') == cleantitle.get(media_title).lower():
                    continue

                headers = {'User_Agent': User_Agent}
                link = client.request(media_url.lower().replace('+','%20'), headers=headers, timeout=10)
                links = link.split('<li id="episode')[1:]
                for p in links:
                    media_url = re.compile('href="([^"]+)"').findall(p)[0]
                    sep = 's%s_e%s' % (season, episode)
                    if sep in media_url.lower():
                        return media_url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User_Agent': User_Agent}
            result = client.request(url.lower().replace('+','%20'), headers=headers, timeout=10)

            rsources = re.findall(r'cale\.html\?r=(.*?)"', str(result), re.I | re.DOTALL)

            uniques = []
            count = 0
            for hosts in rsources:
                final_url = hosts.decode('base64')
                if final_url not in uniques:
                    uniques.append(final_url)

                    host = final_url.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].lower()
                    if not self.filter_host(host):
                        continue
                    host = host.split('.')[0].title()
                    count += 1
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': final_url, 'direct': False, 'debridonly': False})


            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def filter_host(self, host):
        if host not in ['openload.co', 'yourupload.com', 'streamango.com', 'rapidvideo.com']:
            return False
        return True
