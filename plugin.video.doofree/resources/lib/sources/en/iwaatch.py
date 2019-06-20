
import re
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client

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
        regex = '<div class="banner".+?<div class="col-xs-.+?a href="(.+?)".+?div class="post-title">(.+?)<'
        match2 = re.compile(regex, re.DOTALL).findall(response)

        for link_in, title_in in match2:
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