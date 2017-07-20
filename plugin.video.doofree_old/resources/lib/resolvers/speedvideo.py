# -*- coding: utf-8 -*-

import re,base64
from resources.lib.libraries import client


def resolve(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://speedvideo.net/embed-%s.html' % url

        result = client.request(url)

        a = re.compile('var\s+linkfile *= *"(.+?)"').findall(result)[0]
        b = re.compile('var\s+linkfile *= *base64_decode\(.+?\s+(.+?)\)').findall(result)[0]
        c = re.compile('var\s+%s *= *(\d*)' % b).findall(result)[0]

        url = a[:int(c)] + a[(int(c) + 10):]
        url = base64.urlsafe_b64decode(url)
        return url
    except:
        return

