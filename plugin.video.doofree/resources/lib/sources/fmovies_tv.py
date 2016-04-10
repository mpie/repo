# -*- coding: utf-8 -*-

import re,urllib,json,urlparse,xbmc

from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import cleantitle


class source:
    def __init__(self):
        self.base_link = 'http://fmovies.to'
        self.search_link = '/search?keyword=%s'
        self.hash_url = '/ajax/episode/info'
        self.XHR = {'X-Requested-With': 'XMLHttpRequest'}
        self.windowTOKEN = '64.6.102.E.109.7.111.4.118.6.105.5.101.5.115.0.46.6.116.E.111.4.2.8.4.3.3.9.0.3.4.8.0.3.0.7.3.6.4.D.4.5.0.3.0.6.2.C.2.3.0.2.3.6.2.7.3.4.4.F.3.7.1.2.1.3.0.7.2.6.1.C.4.7.0.1.3.3.3.7.0.5.0.4.1.4.1.1.0.4.3.6.4.6.1.9.2.6.3.6.1.2.1.F.4.5.3.4.1.4.4.8.0.3.4.3.0.6.4.E.1.7.2.3.1.3.1.D.1'
        self.windowTOKEN_KEY = 6061

    def get_movie(self, imdb, title, year):
        try:
            url = '%s %s' % (title, year)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self,imdb,tvdb,tvshowtitle,year):
        try:
            url = tvshowtitle
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return
            url = '"%s S%01dE%02d"&type[]=series' % (url, int(season), int(episode))
            url = url.replace("Marvel's ", '')
            url = url.replace("DC's ", '')
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return

    def get_token(self, data):
        n = 0
        for key in data:
            if not key.startswith('_'):
                for i, c in enumerate(data[key]):
                    n += ord(c) * (i + self.windowTOKEN_KEY + len(data[key]))

        return {'_token': hex(n)[2:]}

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            season = re.compile('.*(S\d+).*').findall(url)[0]
            episode = re.compile('.*(E\d+).*').findall(url)[0]
            url = url.replace(' ' + season + episode, '')

            query = self.base_link + self.search_link % url

            result = client.source(query)

            fragments = re.compile('<div class="col-lg-3 col-md-4 col-sm-6 col-xs1-8 col-xs-12">(.+?)</a> </div>').findall(result)

            for fragment in fragments:
                    link = re.compile('class="name" href="(.+?)"').findall(fragment)[0]
                    title = re.compile('class="name" href=".*">(.+)').findall(fragment)[0]
                    is_season = re.compile('class="status">(.+)<span>').findall(fragment)[0]

                    if is_season:
                        season = season.replace('S1', '').replace('S', '')
                        episode = episode.replace('E', '')

                        clean_match_title = cleantitle.tv(title)
                        url = url.replace('&type[]=series', '')
                        clean_original = cleantitle.tv(url+season)
                        original_s1 = url + '1'
                        original_s1 = original_s1.replace(' ','')
                        clean_original_s1 = cleantitle.tv(original_s1)

                        if clean_original == clean_match_title or clean_original_s1 == clean_match_title:
                            result = client.source(link)

                            episode_fragment = re.compile('Server F2 </label> <div class="col-md-20 col-sm-19"> <ul class="episodes">(.+?)</ul>').findall(result)[0]

                            if episode_fragment:
                                episodes = re.compile('data-id="(.+?)" href="(.+?)">(\d+)').findall(episode_fragment)
                                for hash_id, url, epi in episodes:
                                    if epi == episode:
                                        query = {'id': hash_id, 'update': '0'}

                                        query.update(self.get_token(query))
                                        hash_url = self.base_link + self.hash_url + '?' + urllib.urlencode(query)
                                        headers = self.XHR
                                        headers['Referer'] = url
                                        result = client.source(hash_url, headers=headers)

            js_data = json.loads(result)
            links = {}
            link_type = js_data['type']
            target = js_data['target']
            grabber = js_data['grabber']
            params = js_data['params']

            if link_type == 'iframe' and target:
                links[target] = {'direct': False, 'quality': '720p'}
            elif grabber and params:
                links = self.grab_links(grabber, params, url)

            for link in links:
                direct = links[link]['direct']
                quality = links[link]['quality']
                if direct:
                    host = self.get_direct_hostname(link)
                else:
                    host = urlparse.urlparse(link).hostname

                if quality == '720p':
                    quality = 'HD'
                else:
                    quality = 'SD'

                sources.append({'source': host, 'quality': quality, 'provider': 'FMovies', 'url': link})

            return sources
        except:
            return sources

    def get_direct_hostname(self, link):
        host = urlparse.urlparse(link).hostname
        if host and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
            return 'gvideo'
        else:
            return 'fmovies'

    def grab_links(self, grab_url, query, referer):
        try:
            sources = {}
            query['mobile'] = '1'
            query.update(self.get_token(query))
            grab_url = grab_url + '?' + urllib.urlencode(query)
            headers = self.XHR
            headers['Referer'] = referer
            result = client.source(grab_url, headers=headers)
            js_data = json.loads(result)

            if 'data' in js_data:
                for link in js_data['data']:
                    stream_url = link['file']
                    sources[stream_url] = {'direct': True, 'quality': link['label']}
        except:
            pass

        return sources

    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return
