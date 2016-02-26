# -*- coding: utf-8 -*-


import re,urllib,urlparse

from resources.lib import resolvers
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.download_link = 'http://dl.directdlmovie.com/%s'
        self.dvdscr_suffix = '.ShAaNiG.directdlmovie.com.mkv'
        self.hd_suffix = '.directdlmovie.com.mkv'
        self.base_link = 'http://directdlmovie.com'
        self.search_link = '?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            title = title.replace(':', '');

            query = self.search_link % urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, 'div', attrs = {'class': 'thumbn'})
            result = client.parseDOM(result, 'img', ret='alt')

            url = []
            for description in result:
                description = description.replace('.', ' ')
                description = re.sub(' +',' ', description)
                if title in description:
                    filename = description.replace(' ', '.')
                    url.append(filename.encode('utf-8'))

            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            for filename in url:
                try:
                    filename = filename.replace('(','').replace(')', '')
                    file = self.download_link % (filename) + self.hd_suffix

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', filename)
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-|\_', fmt)
                    fmt = [x.lower() for x in fmt]

                    if '1080p' in fmt: quality = '1080p'
                    elif '720p' in fmt or 'hd' in fmt: quality = 'HD'
                    elif 'dvdscr' in fmt:
                        quality = 'SCR'
                        file = self.download_link % (filename) + self.dvdscr_suffix
                    else: quality = 'SD'

                    if '3d' in fmt: info = '3D'
                    else: info = ''

                    sources.append({'source': 'DirectDLMovie', 'quality': quality, 'provider': 'DirectDLMovie', 'url': file, 'info': info})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            u = urlparse.urlparse(url).netloc
            u = u.replace('www.', '').replace('embed.', '')
            u = u.lower()

            if u == 'adf.ly':
                url = resolvers.request(url)

            return url
        except:
            return


