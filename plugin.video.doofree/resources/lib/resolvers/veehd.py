# -*- coding: utf-8 -*-

import re,urllib,urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url, close=False)
        result = result.replace('\n','')

        url = re.compile('function\s*load_download.+?src\s*:\s*"(.+?)"').findall(result)[0]
        url = urlparse.urljoin('http://veehd.com', url)

        result = client.request(url, close=False)

        i = client.parseDOM(result, 'iframe', ret='src')
        if len(i) > 0:
            i = urlparse.urljoin('http://veehd.com', i[0])
            client.request(i, close=False)
            result = client.request(url)

        url = re.compile('href *= *"([^"]+(?:mkv|mp4|avi))"').findall(result)
        url += re.compile('src *= *"([^"]+(?:divx|avi))"').findall(result)
        url += re.compile('"url" *: *"(.+?)"').findall(result)
        url = urllib.unquote(url[0])
        return url
    except:
        return

