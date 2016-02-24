# -*- coding: utf-8 -*-

import re,urllib,urlparse
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client


def resolve(url):
    try:
        result = cloudflare.request(url)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': 'Watch Free!'})
        post = urllib.urlencode(post)

        result = cloudflare.request(url, post=post)
        result = result.replace('\\/', '/').replace('\n', '').replace('\'', '"').replace(' ', '')

        swfUrl = re.compile('\.embedSWF\("(.+?)"').findall(result)[0]
        swfUrl = urlparse.urljoin(url, swfUrl)

        streamer = re.compile('flashvars=.+?"file":"(.+?)"').findall(result)[0]

        playpath = re.compile('flashvars=.+?p2pkey:"(.+?)"').findall(result)[0]

        url = '%s playpath=%s conn=S:%s pageUrl=%s swfUrl=%s swfVfy=true timeout=20' % (streamer, playpath, playpath, url, swfUrl)

        return url
    except:
        return


