# -*- coding: utf-8 -*-

import re
from resources.lib.libraries import client


def resolve(url):
    try:
        url = re.compile('//.+?/.+?/([\w]+)').findall(url)[0]
        url = 'http://www.filepup.net/play/%s' % url

        result = client.request(url)

        url = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
        return url
    except:
        return

