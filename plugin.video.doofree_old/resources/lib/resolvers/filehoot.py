# -*- coding: utf-8 -*-

import re
from resources.lib.libraries import client


def resolve(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://filehoot.com/embed-%s.html' % url

        result = client.request(url, mobile=True)
        url = re.compile('file *: *"(http.+?)"').findall(result)[0]
        return url
    except:
        return

