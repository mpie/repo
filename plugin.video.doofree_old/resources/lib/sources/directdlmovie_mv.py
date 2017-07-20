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
            title = title.replace(':', '')

            query = self.search_link % urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query)

            result = client.request(query)

            thumbs = client.parseDOM(result, 'div', attrs = {'class': 'thumbn'})
            images = client.parseDOM(thumbs, 'img', ret='alt')

            list = client.parseDOM(result, 'li', attrs = {'class': 'izlenme'})
            pages = client.parseDOM(list, 'a', ret='href')

            url = []
            for idx, description in enumerate(images):
                description = description.replace('.', ' ')
                description = description.replace(':', ' ')
                description = re.sub(' +',' ', description)
                description = description.lower()
                title = title.lower()

                if title in description:
                    u = pages[idx]
                    url.append(u.encode('utf-8'))

            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            for p in url:
                result = client.request(p)

                links = re.compile('href="(.+).mkv"').findall(result)
                source = 'directdlmovie'

                if len(links) == 0:
                    links = re.compile('<a href="(.+).mkv" target.+?direct download link').findall(result)
                    source = 'adfly'
                    quality = 'HD'
                    info = ''

                for i in links:
                    try:
                        p = client.replaceHTMLCodes(i)
                        p = p.encode('utf-8')

                        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', i)
                        fmt = re.split('\.|\(|\)|\[|\]|\s|\-|\_', fmt)
                        fmt = [x.lower() for x in fmt]

                        if source not in 'AdFly':
                            if '1080p' in fmt: quality = '1080p'
                            elif '720p' in fmt or 'hd' in fmt: quality = 'HD'
                            else: quality = 'SD'

                            if '3d' in fmt: info = '3D'
                            else: info = ''

                        sources.append({'source': source, 'quality': quality, 'provider': 'DirectDLMovie', 'url': p + '.mkv', 'info': info})
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


