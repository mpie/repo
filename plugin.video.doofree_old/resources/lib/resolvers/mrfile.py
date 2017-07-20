# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'name': 'F1'})[-1]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        url = re.compile('(<a\s+href=.+?>Download\s+.+?</a>)').findall(result)[-1]
        url = client.parseDOM(url, 'a', ret='href')[0]
        return url
    except:
        return

