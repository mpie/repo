# -*- coding: utf-8 -*-

import re,urllib2
from resources.lib.libraries import client


def resolve(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://gorillavid.in/embed-%s.html' % url

        result = client.request(url, mobile=True)
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]

        request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=30)
        response.close()

        type = str(response.info()["Content-Type"])
        if type == 'text/html': raise Exception()

        return url
    except:
        return

