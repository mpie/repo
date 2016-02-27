# -*- coding: utf-8 -*-

import re,urllib,urlparse,random,subprocess,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link_1 = 'https://afdah.org'
        self.base_link_2 = 'https://xmovies8.org'
        self.search_link = '/results?q=%s'
        self.info_link = '/video_info/iframe'


    def get_movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            p = subprocess.Popen(['curl', query], stdout=subprocess.PIPE)
            out, err = p.communicate()

            result = client.parseDOM(out, 'div', attrs = {'class': 'cell_container'})

            title = cleantitle.movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(i[0], re.compile('(.+?) [(](\d{4})[)]').findall(i[1])) for i in result]
            result = [(i[0], i[1][0][0], i[1][0][1]) for i in result if len(i[1]) > 0]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            url = urlparse.urljoin(self.base_link, url)

            p = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
            out, err = p.communicate()

            video_id = re.compile('video_id *= *[\'|\"](.+?)[\'|\"]').findall(out)[0]
            iframeUrl = urlparse.urljoin(self.base_link, self.info_link)

            p = subprocess.Popen(['curl', iframeUrl, '--data', 'v=' + video_id, '-H', 'referer: ' + url], stdout=subprocess.PIPE)
            out, err = p.communicate()

            result = json.loads(out)

            for k,v in result.iteritems():
                if int(k) == 1080:
                    quality = '1080p'
                elif int(k) == 720:
                    quality = 'HD'
                else:
                    quality = 'SD'

                u = v.replace('//html5player.org/embed?url=', '').replace('%3A', ':').replace('%2F', '/').replace('%3D', '=')
                sources.append({'source': 'GVideo', 'quality': quality, 'provider': 'Afdah', 'url': u})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url
