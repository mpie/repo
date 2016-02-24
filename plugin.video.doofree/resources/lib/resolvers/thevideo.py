# -*- coding: utf-8 -*-

import re,ast
from resources.lib.libraries import client


def resolve(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://thevideo.me/embed-%s.html' % url

        result = client.request(url)
        result = result.replace('\n','')

        url = re.compile('file: \'(https?:\/\/.+?\.mp4)\'').findall(result)[-1]
        return url
    except:
        return

