# -*- coding: utf-8 -*-

import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://movietv.to'
        self.headers = {'X-Requested-With': 'XMLHttpRequest'}
        self.search_link = '/search/auto?q=%s'
        self.episode_link = '/series/getLink?id=%s&s=%s&e=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query, headers=self.headers)
            result = json.loads(result)

            title = cleantitle.movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(i['link'], i['title'], str(i['year'])) for i in result]
            result = [i for i in result if '/movies/' in i[0]]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.search_link % urllib.quote_plus(tvshowtitle)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query, headers=self.headers)
            result = json.loads(result)

            tvshowtitle = cleantitle.tv(tvshowtitle)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(i['link'], i['title'], str(i['year'])) for i in result]
            result = [i for i in result if '/series/' in i[0]]
            result = [i for i in result if tvshowtitle == cleantitle.tv(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            if not '%01d' % int(season) == '1': return
            if '%01d' % int(episode) > '3': return

            url += '?S%02dE%02d' % (int(season), int(episode))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            content = re.compile('(.+?)\?S\d*E\d*$').findall(url)

            try: url, season, episode = re.compile('(.+?)\?S(\d*)E(\d*)$').findall(url)[0]
            except: pass

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)

            if len(content) == 0:
                u = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
            else:
                u = re.compile('playSeries\((\d+),(%01d),(%01d)\)' % (int(season), int(episode))).findall(result)[0]
                u = self.episode_link % (u[0], u[1], u[2])
                u = urlparse.urljoin(self.base_link, u)
                u = client.source(u)
                u = json.loads(u)['url']

            url = '%s|User-Agent=%s&Referer=%s' % (u, urllib.quote_plus(client.agent()), urllib.quote_plus(url))

            sources.append({'source': 'MovieTV', 'quality': 'HD', 'provider': 'MovieTV', 'url': url})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


