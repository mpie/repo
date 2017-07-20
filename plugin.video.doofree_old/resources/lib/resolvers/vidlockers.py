# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client


def resolve(url):
    try:
        cookie = client.request(url, output='cookie')
        result = client.request(url, cookie=cookie, close=False)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'method': 'POST'})[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        url = re.compile("file *: *'(http.+?)'").findall(result)
        url += re.compile('file *: *"(http.+?)"').findall(result)
        url = [i for i in url if not i.endswith('.srt')]
        url = url[-1]

        return url
    except:
        return

