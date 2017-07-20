# -*- coding: utf-8 -*-

import re,urlparse,json
from resources.lib.libraries import client


def resolve(url):
    try:
        channel = re.compile('[/v/|/view#]([\w]+)').findall(url)[-1]

        url = 'http://veetle.com/index.php/stream/ajaxStreamLocation/%s/android-hls' % channel
        result = client.request(url, mobile=True)
        url = json.loads(result)

        m3u8 = url['payload']

        url = client.request(m3u8).splitlines()
        url = [i for i in url if '.m3u8' in i]
        if len(url) == 0: return m3u8
        url = urlparse.urljoin(m3u8, url[0])

        return url
    except:
        return

