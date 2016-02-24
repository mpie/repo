# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries import captcha


def resolve(url):
    try:
        result = client.request(url)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': ''})
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': 'Free Download'})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': 'Free Download'})
        try: post.update(captcha.request(result))
        except: pass
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        url = client.parseDOM(result, 'a', ret='onClick')
        url = [i for i in url if i.startswith('window.open')][0]
        url = re.compile('[\'|\"](.+?)[\'|\"]').findall(url)[0]
        return url
    except:
        return

