# -*- coding: utf-8 -*-

import re, base64
from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url, mobile=True)

        ysmm = re.compile('var ysmm = \'(.+)\';').findall(result)[0]
        a = ''
        t = ''
        for i in range(len(ysmm)):
            if i % 2 == 0:
                a += ysmm[i]
            else:
                t = ysmm[i] + t

        url = base64.b64decode(a + t)
        url = url.replace(' ', '%20')[2:]

        return url
    except:
        return

