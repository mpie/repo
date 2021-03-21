
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
        self.search_link = 'https://iwaatch.com/api/api.php?page=moviesearch&q=%s'
        self.sources2 = []

    def movie(self, imdb, title, localtitle, aliases, year):
        clean_title = cleantitle.geturl(title).replace('-', '%20').replace('None', '')
        url = urlparse.urljoin(self.base_link, (self.search_link % clean_title)) + '$$$$$' + clean_title
        return url

    def sources(self, url, hostDict, hostprDict):
        self.sources2 = []

        if url is None:
            return self.sources2

        data = url.split('$$$$$')

        url = data[0]
        title = data[1].replace('\'', '')

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
        regex = "href=\"(.+?)\">\n.+\n\s+(.+)\n.+>(.+?)<"
        r = re.findall(regex, response)

        for links in r:
            if title == cleantitle.geturl(links[1]).replace('-', '%20'):
                x = client.request(links[0].replace('movie', 'view'), headers=headers)
                regex = "src:.+'(.+?)',.+\n.+\n.+size:.+'(.+)'"
                match3 = re.findall(regex, x)

                for url in match3:
                    self.sources2.append(
                        {'source': 'Direct', 'quality': url[1] + 'p', 'language': 'en', 'url': url[0] + '|Referer=https://iwaatch.com/view/' + title, 'direct': True, 'debridonly': False})

        return self.sources2

    def resolve(self, url):
        return url