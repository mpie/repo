# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client


def resolve(url):
    try:
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://streamcloud.eu/%s' % url
 
        result = client.request(url)

        post = {}
        f = client.parseDOM(result, 'form', attrs = {'class': 'proform'})[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post = urllib.urlencode(post)
        post = post.replace('op=download1', 'op=download2')

        result = client.request(url, post=post)

        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

