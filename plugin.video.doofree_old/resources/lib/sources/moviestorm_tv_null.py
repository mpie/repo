# -*- coding: utf-8 -*-

import re,urllib,urlparse

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://moviestorm.eu'
        self.tvsearch_link = '/series/all/'
        self.episode_link = '%s?season=%01d&episode=%01d'


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = urlparse.urljoin(self.base_link, self.tvsearch_link)

            result = client.source(query)

            tvshowtitle = cleantitle.tv(tvshowtitle)

            result = zip(client.parseDOM(result, 'a', {'class': 'underilne'}, 'href'), client.parseDOM(result, 'a', {'class': 'underilne'}))
            result = [i[0] for i in result if tvshowtitle == cleantitle.tv(i[1])][0]
            check = urlparse.urljoin(self.base_link, result)
            check = client.source(check)
            if not str(imdb) in check: raise Exception()

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return

        url = self.episode_link % (url, int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)
            result = client.parseDOM(result, 'div', attrs = {'class': 'links'})[0]
            result = client.parseDOM(result, 'tr')
            result = [(client.parseDOM(i, 'td', attrs = {'class': 'quality_td'})[0], client.parseDOM(i, 'a', ret='href')[-1]) for i in result]

            ts_quality = ['CAM', 'TS']
            links = [i for i in result if not any(x in i[0] for x in ts_quality)]
            if len(links) == 0: links = result

            for i in links:
                try:
                    url = i[1]
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.sub('.+?/exit/\d*-|[.].+?[.]html|http://(|www[.])|/.+|[.].+$','', i[1])
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    if any(x in i[0] for x in ts_quality): quality = 'CAM'
                    else: quality = 'SD'

                    sources.append({'source': host, 'quality': quality, 'provider': 'Moviestorm', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if url.startswith(self.base_link):
                result = client.request(url)
                url = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'real_link'})[0]

            url = resolvers.request(url)
            return url
        except:
            return


