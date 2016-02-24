# -*- coding: utf-8 -*-

import re
from resources.lib.libraries import client


def resolve(url):
    try:
        id = re.compile('//.+?/.+?/([\w]+)').findall(url)
        id += re.compile('//.+?/.+?v=([\w]+)').findall(url)
        id = id[0]

        url = 'http://embed.videoweed.es/embed.php?v=%s' % id

        result = client.request(url)

        key = re.compile('flashvars.filekey=(.+?);').findall(result)[-1]
        try: key = re.compile('\s+%s="(.+?)"' % key).findall(result)[-1]
        except: pass

        url = 'http://www.videoweed.es/api/player.api.php?key=%s&file=%s' % (key, id)
        result = client.request(url)

        url = re.compile('url=(.+?)&').findall(result)[0]
        return url
    except:
        return

