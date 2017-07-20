# -*- coding: utf-8 -*-

import re
from resources.lib.libraries import client


def resolve(url):
        try:
            url = url.replace('/share/file/', '/embed/')
            result = client.request(url)
            url = re.compile('var\s+vurl *= *"(http.+?)"').findall(result)[0]
            return url
        except:
            return

