# -*- coding: utf-8 -*-

import urllib,urllib2,time
from resources.lib.libraries import client
from resources.lib.libraries import captcha


def resolve(url):
    try:
        result = client.request(url, close=False)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update(captcha.request(result))
        post = urllib.urlencode(post)

        request = urllib2.Request(url, post)

        for i in range(0, 5):
            try:
                response = urllib2.urlopen(request, timeout=10)
                result = response.read()
                response.close()
                if 'download2' in result: raise Exception()
                url = client.parseDOM(result, 'a', ret='href', attrs = {'target': ''})[0]
                return url
            except:
                time.sleep(1)
    except:
        return

