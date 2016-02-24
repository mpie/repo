# -*- coding: utf-8 -*-

import re,urlparse,json

from resources.lib.libraries import client
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://mvsnap.com/'
        self.search_link = '/v1/api/search?query=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % imdb
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = json.loads(result)
            result = result['movies'][0]['slug']

            url = '/movies/%s' % result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = '%s (%s)' % (tvshowtitle, year)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            query = self.search_link % imdb
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = json.loads(result)
            result = result['movies']

            season = '%02d' % int(season)
            episode = '%02d' % int(episode)

            result = [(i['slug'], i['long_title']) for i in result]
            result = [(i[0], re.compile('(\d*)$').findall(i[1])) for i in result]
            result = [(i[0], i[1][0]) for i in result if len(i[1]) > 0]
            result = [i[0] for i in result if season == i[1]][0]

            url = '/tv-shows/%s?S%sE%s' % (result, season, episode)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            query = urlparse.urlparse(url).query
            try: query = '%02d' % int(re.compile('E(\d*)$').findall(query)[0])
            except: query = ''

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)

            result = client.parseDOM(result, 'select', attrs = {'id': 'myDropdown'})[0]
            result = zip(client.parseDOM(result, 'option', ret='value'), client.parseDOM(result, 'option'))
            result = [i[0] for i in result if query.endswith(i[1]) or query == ''][0]

            url = urlparse.urljoin(self.base_link, result)

            url = client.source(url, output='geturl')
            if not 'google' in url: raise Exception()

            url = url.split('get_video_info')[0]
            url = resolvers.request(url)

            for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'MVsnap', 'url': i['url']})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


