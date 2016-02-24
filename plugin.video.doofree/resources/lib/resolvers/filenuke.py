# -*- coding: utf-8 -*-

import re,urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url, close=False)

        f = client.parseDOM(result, 'a', ret='href', attrs = {'id': 'go-next'})[0]
        f = urlparse.urljoin(url, f)

        result = client.request(f)

        url = re.compile("var\s+lnk\d* *= *'(http.+?)'").findall(result)[0]
        return url
    except:
        return

