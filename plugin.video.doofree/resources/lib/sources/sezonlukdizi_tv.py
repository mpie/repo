# -*- coding: utf-8 -*-


import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache


class source:
    def __init__(self):
        self.domains = ['sezonlukdizi.com']
        self.base_link = 'http://sezonlukdizi.com'
        self.search_link = '/js/dizi.js'
        self.video_link = '/ajax/dataEmbed.asp'


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            result = cache.get(self.sezonlukdizi_tvcache, 120)

            tvshowtitle = cleantitle.get(tvshowtitle)

            result = [i[0] for i in result if tvshowtitle == i[1]][0]

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sezonlukdizi_tvcache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)

            for i in range(3):
                result = client.request(url)
                if not result == None: break

            result = re.compile('{(.+?)}').findall(result)
            result = [(re.findall('u\s*:\s*(?:\'|\")(.+?)(?:\'|\")', i), re.findall('d\s*:\s*(?:\'|\")(.+?)(?:\'|\")', i)) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(re.compile('/diziler(/.+?)(?://|\.|$)').findall(i[0]), re.sub('&#\d*;','', i[1])) for i in result]
            result = [(i[0][0] + '/', cleantitle.get(i[1])) for i in result if len(i[0]) > 0]

            return result
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return

        url = '%s%01d-sezon-%01d-bolum.html' % (url.replace('.html', ''), int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hostDict, hostprDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            for i in range(3):
                result = client.request(url)
                if not result == None: break

            result = re.sub(r'[^\x00-\x7F]+', ' ', result)

            pages = []

            r = client.parseDOM(result, 'div', attrs = {'id': 'embed'})[0]
            pages.append(client.parseDOM(r, 'iframe', ret='src')[0])


            for page in pages:
                try:
                    for i in range(3):
                        result = client.request(page)
                        if not result == None: break

                    captions = re.search('kind\s*:\s*(?:\'|\")captions(?:\'|\")', result)
                    if not captions: raise Exception()

                    try:
                        r = re.findall('url\s*:\s*\'(http(?:s|)://api.pcloud.com/.+?)\'', result)[0]
                        r = client.request(r)
                        r = json.loads(r)['variants']
                        r = [(i['hosts'], i['path'], i['height']) for i in r if 'hosts' in i and 'path' in i and 'height' in i]
                        r = [('%s%s' % (i[0][0], i[1]), str(i[2])) for i in r if len(i[0]) > 0]
                        r = [(i[0] if i[0].startswith('http') else 'http://%s' % i[0], i[1]) for i in r]
                        host = 'cdn' ; direct = False ; l = r
                    except:
                        pass

                    try:
                        r = re.findall('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?[^"]*"', result)
                        if not r: raise Exception()
                        host = 'gvideo' ; direct = True ; l = r
                    except:
                        pass

                    links = [(i[0], '1080p') for i in l if int(i[1]) >= 1080]
                    links += [(i[0], 'HD') for i in l if 720 <= int(i[1]) < 1080]
                    links += [(i[0], 'SD') for i in l if 480 <= int(i[1]) < 720]

                    for i in links: sources.append({'source': host, 'quality': i[1], 'provider': 'Sezonlukdizi', 'url': i[0], 'direct': direct, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


