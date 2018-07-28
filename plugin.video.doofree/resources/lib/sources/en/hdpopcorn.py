# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdpopcorns.com']
        self.base_link = 'http://hdpopcorns.com'
        self.search_link = '/search/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year']

            search_id = cleantitle.getsearch(title.lower())
            query = urlparse.urljoin(self.base_link, self.search_link % (search_id.replace(' ','+')))
            result = client.request(query, timeout=3)

            links = re.compile('<header>.+?href="(.+?)" title="(.+?)"', re.DOTALL).findall(result)
            for m_url, m_title in links:
                if cleantitle.getsearch(title).lower() in cleantitle.getsearch(m_title).lower():
                    if year in m_title:
                        headers = {'Origin': 'http://hdpopcorns.com', 'Referer': m_url, 'X-Requested-With': 'XMLHttpRequest'}
                        result = client.request(m_url)

                        try:
                            params = re.compile('FileName1080p.+?value="(.+?)".+?FileSize1080p.+?value="(.+?)".+?value="(.+?)"', re.DOTALL).findall(result)
                            for param1, param2, param3 in params:
                                request_url = '%s/select-movie-quality.php' % (self.base_link)
                                form_data = {'FileName1080p': param1, 'FileSize1080p': param2, 'FSID1080p': param3}
                            link = client.request(request_url, post=form_data, headers=headers, timeout=3)
                            final_url = re.compile('<strong>1080p</strong>.+?href="(.+?)"', re.DOTALL).findall(link)[0]
                            res = '1080p'
                            sources.append({'source': 'CDN', 'quality': res, 'language': 'en', 'url': final_url, 'direct': True, 'debridonly': False})
                        except:
                            pass
                        try:
                            params = re.compile('FileName720p.+?value="(.+?)".+?FileSize720p".+?value="(.+?)".+?value="(.+?)"', re.DOTALL).findall(result)
                            for param1, param2, param3 in params:
                                request_url = '%s/select-movie-quality.php' % (self.base_link)
                                form_data = {'FileName720p': param1, 'FileSize720p': param2, 'FSID720p': param3}
                            link = client.request(request_url, post=form_data, headers=headers, timeout=3)
                            final_url = re.compile('<strong>720p</strong>.+?href="(.+?)"', re.DOTALL).findall(link)[0]
                            res = '720p'
                            sources.append({'source': 'CDN', 'quality': res, 'language': 'en', 'url': final_url, 'direct': True, 'debridonly': False})
                        except:
                            pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url



