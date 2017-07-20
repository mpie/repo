# -*- coding: utf-8 -*-

import urllib,time
from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url)

        post = {}
        f = client.parseDOM(result, 'form', attrs = {'name': 'F1'})[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post = urllib.urlencode(post)

        for i in range(0, 3):
            try:
                result = client.request(url, post=post)
                url = client.parseDOM(result, 'div', attrs = {'align': '.+?'})
                url = [i for i in url if 'button_upload' in i][0]
                url = client.parseDOM(url, 'a', ret='href')[0]
                url = ['http' + i for i in url.split('http') if 'uptobox.com' in i][0]
                return url
            except:
                time.sleep(1)
    except:
        return


def check(url):
    try:
        result = client.request(url)
        if result == None: return False

        result = client.parseDOM(result, 'span', attrs = {'class': 'para_title'})
        if any('File not found' in x for x in result): raise Exception()

        return True
    except:
        return False


