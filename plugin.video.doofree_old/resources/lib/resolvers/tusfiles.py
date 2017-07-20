# -*- coding: utf-8 -*-

import re,urlparse
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        result = client.request(url)

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack.unpack(result)

        url = client.parseDOM(result, 'embed', ret='src')
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url = [i for i in url if not i.endswith('.srt')]
        url = 'http://' + url[0].split('://', 1)[-1]

        url = url.replace(':%s' % urlparse.urlparse(url).port, '')

        return url
    except:
        return

