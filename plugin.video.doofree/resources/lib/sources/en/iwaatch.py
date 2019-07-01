
import re
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['iwaatch.com']
        self.base_link = 'https://iwaatch.com/'
        self.search_link = 'https://iwaatch.com/?q=%s'
        self.sources2 = []

    def movie(self, imdb, title, localtitle, aliases, year):
        if 1:  # try:
            clean_title = cleantitle.geturl(title).replace('-', '%20')
            url = urlparse.urljoin(self.base_link, (
            self.search_link % (clean_title))) + '$$$$$' + title + '$$$$$' + year + '$$$$$' + 'movie'
            return url
            # except:
            #    return

    def sources(self, url, hostDict, hostprDict):
        self.sources2 = []

        if url is None:
            return self.sources2

        data = url.split('$$$$$')

        url = data[0]
        title = data[1]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'identity;q=1, *;q=0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'DNT': '1'
        }

        response = client.request(url, headers=headers)
        r = dom_parser.parse_dom(response, 'div', attrs={'class': ['col-xs-12', 'col-sm-6', 'col-md-3']})
        r = dom_parser.parse_dom(r, 'a', req='href')
        r = [(i.attrs['href'], i.content) for i in r if i]
        r = [(i[0], re.findall('<div class="post-title">(.+?)</div>', i[1], re.IGNORECASE)) for i in r]

        for link_in, title_in in r:
            if title in title_in:
                x = client.request(link_in.replace('movie', 'view'), headers=headers)
                regex = "file: '(.+?)'.+?label: '(.+?)'"
                match3 = re.compile(regex, re.DOTALL).findall(x)

                for url, q in match3:
                    self.sources2.append(
                        {'source': 'Direct', 'quality': q, 'language': 'en', 'url': url+'|Referer=https://iwaatch.com/view/' + title, 'direct': True, 'debridonly': False})

        return self.sources2

    def resolve(self, url):
        return url