# -*- coding: utf-8 -*-


import re,urllib,urlparse

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://directdlmovie.com'
        self.search_link = '?s=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, 'li', attrs = {'class': 'izlenme'})
            result = client.parseDOM(result, 'a', ret='href')[0]

            url = re.compile('//.+?/(.+)').findall(result)[0]
            url = url.encode('utf-8')

            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, '/' + url)

            result = client.source(url)

            links = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'emd_dl_green_light'})

            for i in links:
                try:
                    url = client.replaceHTMLCodes(i)
                    url = url.encode('utf-8')

                    if not url.endswith(('mp4', 'mkv')): raise Exception()

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', i)
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-|\_', fmt)
                    fmt = [x.lower() for x in fmt]

                    if '1080p' in fmt: quality = '1080p'
                    elif '720p' in fmt or 'hd' in fmt: quality = 'HD'
                    else: quality = 'SD'

                    if '3d' in fmt: info = '3D'
                    else: info = ''

                    sources.append({'source': 'DirectDLMovie', 'quality': quality, 'provider': 'DirectDLMovie', 'url': url, 'info': info})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):

        try:
            content = re.compile('(.+?)\?S\d*E\d*$').findall(url)

            if len(content) == 0: return url

            url, season, episode = re.compile('(.+?)\?S(\d*)E(\d*)$').findall(url)[0]

            match = ['S%sE%s' % (season, episode), 'S%s E%s' % (season, episode)]

            result = client.source(url)
            result = client.parseDOM(result, 'a', ret='href')
            result = [i for i in result if any(x in i for x in match)][0]

            url = '%s/%s' % (url, result)
            return url
        except:
            return


