# -*- coding: utf-8 -*-

import json
from resources.lib.libraries import client


def resolve(url):
    try:
        url = [i for i in url.split('/') if i.isdigit()][-1]
        url = 'http://player.vimeo.com/video/%s/config' % url

        result = client.request(url)
        result = json.loads(result)
        u = result['request']['files']['h264']

        url = None
        try: url = u['hd']['url']
        except: pass
        try: url = u['sd']['url']
        except: pass

        return url
    except:
        return

