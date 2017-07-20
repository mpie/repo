# -*- coding: utf-8 -*-

from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url, mobile=True)
        url = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
        return url
    except:
        return

