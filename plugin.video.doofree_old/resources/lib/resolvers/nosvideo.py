# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client


def resolve(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]

        u = 'http://nosvideo.com/vj/video.php?u=%s&w=&h=530' % url
        r = 'http://nosvideo.com/%s' % url

        result = client.request(u, referer=r)

        url = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video/.+?'})
        url += client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video/mp4'})
        url = url[-1]

        return url
    except:
        return

