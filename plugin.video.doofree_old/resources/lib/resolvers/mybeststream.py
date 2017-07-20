# -*- coding: utf-8 -*-

import re,urlparse
from resources.lib.libraries import client
from resources.lib.libraries import unwise


def resolve(url):
    try:
        referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        page = url.replace(referer, '').replace('&referer=', '').replace('referer=', '')

        result = client.request(url, referer=referer)
        result = re.compile("}[(]('.+?' *, *'.+?' *, *'.+?' *, *'.+?')[)]").findall(result)[-1]
        result = unwise.execute(result)

        strm = re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        strm = [i for i in strm if i.startswith('rtmp')][0]
        url = '%s pageUrl=%s live=1 timeout=10' % (strm, page)
        return url
    except:
        return

