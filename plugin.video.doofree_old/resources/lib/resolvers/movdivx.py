# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://www.movdivx.com/%s' % url
 
        result = client.request(url)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })[0]
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': 'Free Download'})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack.unpack(result)

        url = client.parseDOM(result, 'embed', ret='src')
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url = [i for i in url if not i.endswith('.srt')]
        url = 'http://' + url[0].split('://', 1)[-1]

        return url
    except:
        return

