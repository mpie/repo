# -*- coding: utf-8 -*-

import re
from resources.lib.libraries import client


def resolve(url):
    try:
        result = client.request(url)
        url = re.compile("file *: *'(http.+?)'").findall(result)[-1]
        return url
    except:
        return

