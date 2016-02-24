# -*- coding: utf-8 -*-

import urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        url = urlparse.urlparse(url).query
        url = urlparse.parse_qsl(url)[0][1]
        url = 'http://up2stream.com/view.php?ref=%s' % url

        result = client.request(url, mobile=True)

        url = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
        return url
    except:
        return

