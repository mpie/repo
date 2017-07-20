# -*- coding: utf-8 -*-

import urllib
from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url)

        post = {}
        f = client.parseDOM(result, 'form', attrs = {'method': 'post'})[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        url = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'view_dl_link'})[0]
        url = client.request(url, output='geturl', post=post)
        return url
    except:
        return

