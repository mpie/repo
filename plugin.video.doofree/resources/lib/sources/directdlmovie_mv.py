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
            thumbs = client.parseDOM(result, 'div', attrs = {'class': 'thumbn'})
            images = client.parseDOM(thumbs, 'img', ret='alt')

            list = client.parseDOM(result, 'li', attrs = {'class': 'izlenme'})
            pages = client.parseDOM(list, 'a', ret='href')

            url = []
            for idx, description in enumerate(images):
                description = description.replace('.', ' ')
                description = re.sub(' +',' ', description)

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
                result = client.source(p)

                links = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'emd_dl_green_light'})
                source = 'DirectDLMovie'

                if len(links) == 0:
                    links = re.compile('<a href="(.+)" target.+?direct download link').findall(result)
                    source = 'AdFly'

                for i in links:
                    try:
                        p = client.replaceHTMLCodes(i)
                        p = p.encode('utf-8')

                        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', i)
                        fmt = re.split('\.|\(|\)|\[|\]|\s|\-|\_', fmt)
                        fmt = [x.lower() for x in fmt]

                        if '1080p' in fmt: quality = '1080p'
                        elif '720p' in fmt or 'hd' in fmt: quality = 'HD'
                        else: quality = 'SD'

                        if '3d' in fmt: info = '3D'
                        else: info = ''

                        sources.append({'source': source, 'quality': quality, 'provider': 'DirectDLMovie', 'url': p, 'info': info})
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


