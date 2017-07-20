# -*- coding: utf-8 -*-

import re
from resources.lib.libraries import client


def resolve(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://vodlocker.com/embed-%s.html' % url

        result = client.request(url)

        url = re.compile('[\'|\"](http.+?[\w]+)[\'|\"]').findall(result)
        url = [i for i in url if i.endswith(('.mp4', '.mkv', '.flv', '.avi'))][0]
        return url
    except:
        return

