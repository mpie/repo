# -*- coding: utf-8 -*-

import re,urllib,urlparse,json,base64

from resources.lib.libraries import directstream
from resources.lib.libraries import client
from resources.lib.libraries import cache


class source:
    def __init__(self):
        self.domains = ['pubfilmno1.com', 'pubfilm.com', 'pidtv.com', 'pubfilm.ac']
        self.base_link = 'http://pubfilm.ac'
        self.moviesearch_link = '/%s-%s-full-hd-pubfilm-free.html'
        self.moviesearch_link_2 = '/%s-%s-pubfilm-free.html'
        self.tvsearch_link = '/wp-admin/admin-ajax.php'
        self.tvsearch_link_2 = '/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            title = (title.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()

            query = self.moviesearch_link % (title, year)
            query = urlparse.urljoin(self.base_link, query)

            result = client.request(query)

            if result == None:
                query = self.moviesearch_link_2 % (title, year)
                query = urlparse.urljoin(self.base_link, query)

                result = client.request(query, limit='5')

            if result == None:
                raise Exception()

            url = re.findall('(?://.+?|)(/.+)', query)[0]
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            year = re.findall('(\d{4})', premiered)[0]
            season = '%01d' % int(season) ; episode = '%01d' % int(episode)
            tvshowtitle = '%s %s: Season %s' % (data['tvshowtitle'], year, season)

            url = cache.get(self.pidtv_tvcache, 120, tvshowtitle)

            if url == None: raise Exception()

            url += '?episode=%01d' % int(episode)
            url = url.encode('utf-8')
            return url
        except:
            return

    def pidtv_tvcache(self, tvshowtitle):
        try:
            post = urllib.urlencode({'aspp': tvshowtitle, 'action': 'ajaxsearchpro_search', 'options': 'qtranslate_lang=0&set_exactonly=checked&set_intitle=None&customset%5B%5D=post', 'asid': '5', 'asp_inst_id': '5_1'})
            url = urlparse.urljoin(self.base_link, self.tvsearch_link)
            url = client.request(url, post=post, XHR=True)
            url = zip(client.parseDOM(url, 'a', ret='href', attrs={'class': 'asp_res_url'}), client.parseDOM(url, 'a', attrs={'class': 'asp_res_url'}))
            url = [(i[0], re.findall('(.+?: Season \d+)', i[1].strip())) for i in url]
            url = [i[0] for i in url if len(i[1]) > 0 and tvshowtitle == i[1][0]][0]

            url = urlparse.urljoin(self.base_link, url)
            url = re.findall('(?://.+?|)(/.+)', url)[0]
            return url
        except:
            return

    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            content = re.compile('(.+?)\?episode=\d*$').findall(url)
            content = 'movie' if len(content) == 0 else 'episode'

            try: url, episode = re.compile('(.+?)\?episode=(\d*)$').findall(url)[0]
            except: pass

            result = client.request(url)
            result = result.replace('"target="EZWebPlayer"', '" target="EZWebPlayer"')
            url = zip(client.parseDOM(result, 'a', ret='href', attrs={'target': 'EZWebPlayer'}), client.parseDOM(result, 'a', attrs={'target': 'EZWebPlayer'}))
            url = [(i[0], re.compile('(\d+)').findall(i[1])) for i in url]
            url = [(i[0], i[1][-1]) for i in url if len(i[1]) > 0]

            if content == 'episode':
                url = [i for i in url if i[1] == '%01d' % int(episode)]

            links = [client.replaceHTMLCodes(i[0]) for i in url]


            for u in links:
                try:
                    result = client.request(u)
                    result = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    result = re.findall('"file"\s*:\s*"(.+?)"', result)

                    for url in result:
                        try:
                            url = url.replace('\\', '')
                            url = directstream.googletag(url)[0]
                            sources.append({'source': 'gvideo', 'quality': url['quality'], 'provider': 'Pubfilm', 'url': url['url'], 'direct': True, 'debridonly': False})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return directstream.googlepass(url)


