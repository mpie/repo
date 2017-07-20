# -*- coding: utf-8 -*-

from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url, mobile=True)

        url = client.parseDOM(result, 'video')[0]
        url = client.parseDOM(url, 'source', ret='src', attrs = {'type': '.+?'})[0]
        return url
    except:
        return

