# -*- coding: utf-8 -*-


import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://www.dizigold.net'
        self.headers = {'X-Requested-With': 'XMLHttpRequest'}
        self.ajax_link = '/sistem/ajax.php'
        self.search_link = 'aranan=%s&tip=aranans'
        self.episode_link = 'sezon_id=%s&dizi_id=%s&tip=sezon'
        self.player_link = 'id=%s&tip=view&dil=or'
        self.iframe_link = 'http://player.dizigold.net/?id=%s&s=1&dil=or'


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            return tvshowtitle
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = '%s/%01d-sezon/%01d-bolum' % (url.replace(' ', '-').lower(), int(season), int(episode))
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)

            post = re.compile('var\s*view_id\s*=\s*"(\d*)"').findall(result)[0]
            url = self.iframe_link % post
            result = client.source(url, headers=self.headers)

            result = re.compile('"file"\s*:\s*"(.+?)".+?"label"\s*:\s*"(\d*p)"').findall(result)

            links = [{'url': i[0], 'quality': i[1]} for i in result if 'google' in i[0]]
            links += [{'url': '%s|User-Agent=%s&Referer=%s' % (i[0], urllib.quote_plus(client.agent()), urllib.quote_plus(url)), 'quality': i[1]} for i in result if not 'google' in i[0]]

            try: sources.append({'source': 'GVideo', 'quality': '1080p', 'provider': 'Dizigold', 'url': [i['url'] for i in links if i['quality'] == '1080p'][0]})
            except: pass
            try: sources.append({'source': 'GVideo', 'quality': 'HD', 'provider': 'Dizigold', 'url': [i['url'] for i in links if i['quality'] == '720p'][0]})
            except: pass
            try: sources.append({'source': 'GVideo', 'quality': 'SD', 'provider': 'Dizigold', 'url': [i['url'] for i in links if i['quality'] == '480p'][0]})
            except: sources.append({'source': 'GVideo', 'quality': 'SD', 'provider': 'Dizigold', 'url': [i['url'] for i in links if i['quality'] == '360p'][0]})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if not 'google' in url: return url
            if url.startswith('stack://'): return url

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

