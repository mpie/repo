# -*- coding: utf-8 -*-

import re
from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url, mobile=True)
        url = re.compile('file *: *"(http.+?)"').findall(result)[0]
        return url
    except:
        return

