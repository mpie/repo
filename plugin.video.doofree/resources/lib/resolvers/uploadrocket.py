# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries import captcha


def resolve(url):
    try:
        result = client.request(url)
        result = result.decode('iso-8859-1').encode('utf-8')

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'name': 'freeorpremium'})[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_isfree': 'Click for Free Download'})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)
        result = result.decode('iso-8859-1').encode('utf-8')

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'name': 'F1'})[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update(captcha.request(result))
        post = urllib.urlencode(post)

        result = client.request(url, post=post)
        result = result.decode('iso-8859-1').encode('utf-8')

        url = client.parseDOM(result, 'a', ret='href', attrs = {'onclick': 'DL.+?'})[0]
        return url
    except:
        return


def check(url):
    try:
        base = 'http://uploadrocket.net/?op=checkfiles'
        post = urllib.urlencode({'op': 'checkfiles', 'process': 'Check URLs', 'list': url})

        result = client.request(base, post=post)
        if result == None: return False

        result = client.parseDOM(result, 'Table', attrs = {'class': 'tbl1'})[0]
        result = client.parseDOM(result, 'td', attrs = {'style': '.+?'})[0]
        if 'Not found' in result: return False

        return True
    except:
        return False


