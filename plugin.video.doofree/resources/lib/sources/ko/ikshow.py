# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 DooFree
'''

import re,urllib,urlparse,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['ko']
        self.domains = ['ikshow.net']
        self.base_link = 'http://ikshow.net'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
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

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                url = '%s/shows/%s/episode-%01d/' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['episode']))

                url = client.request(url, timeout='10', output='geturl')
                if url == None: raise Exception()

            else:
                url = urlparse.urljoin(self.base_link, url)
                r = client.request(url, timeout='10')

            r = client.request(url, timeout='10')
            links = client.parseDOM(r, 'iframe', ret='src')

            for link in links:
                if 'vidnow' in link:
                    r = client.request(link, timeout='10')
                    r = re.findall('(https:.*?(openload|redirector).*?)[\'\"]', r)

                    for i in r:
                        if 'openload' in i:
                            try: sources.append({'source': 'openload', 'quality': 'SD', 'language': 'ko', 'url': i[0], 'direct': False, 'debridonly': False})
                            except: pass
                        elif 'google' in i:
                            try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'ko', 'url': i[0], 'direct': True, 'debridonly': False})
                            except: pass
                        else: pass
                else: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        if "google" in url:
            return directstream.googlepass(url)
        else:
            return url


