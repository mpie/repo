# -*- coding: utf-8 -*-

import re
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://www.mightyupload.com/embed-%s.html' % url

        result = client.request(url, mobile=True)

        url = re.compile("file *: *'(.+?)'").findall(result)
        if len(url) > 0: return url[0]

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack.unpack(result)

        url = client.parseDOM(result, 'embed', ret='src')
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url = [i for i in url if not i.endswith('.srt')]
        url = 'http://' + url[0].split('://', 1)[-1]

        return url
    except:
        return

