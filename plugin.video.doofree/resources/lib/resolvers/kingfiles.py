# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries import captcha


def resolve(url):
    try:
        result = client.request(url)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': ' '})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': ' '})
        post.update(captcha.request(result))
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        url = re.compile("var\s+download_url *= *'(.+?)'").findall(result)[0]
        return url
    except:
        return

