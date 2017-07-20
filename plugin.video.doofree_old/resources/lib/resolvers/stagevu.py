# -*- coding: utf-8 -*-

from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url)

        url = client.parseDOM(result, 'embed', ret='src', attrs = {'type': 'video.+?'})[0]
        return url
    except:
        return

