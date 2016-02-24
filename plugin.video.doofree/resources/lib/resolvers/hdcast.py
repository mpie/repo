# -*- coding: utf-8 -*-

import re,urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]

        pageUrl = 'http://hdcast.me/embedplayer.php?id=%s&autoplay=true' % id
        swfUrl = 'http://p.jwpcdn.com/6/12/jwplayer.flash.swf'

        result = client.request(pageUrl, referer=pageUrl)

        streamer = result.replace('//file', '')
        streamer = re.compile("file *: *'(.+?)'").findall(streamer)[-1]

        token = re.compile('getJSON[(]"(.+?)".+?json[.]token').findall(result.replace('\n', ''))[-1]
        token = client.request(token, referer=pageUrl)
        token = re.compile('"token" *: *"(.+?)"').findall(token)[-1]

        url = '%s pageUrl=%s swfUrl=%s token=%s live=true timeout=20' % (streamer, pageUrl, swfUrl, token)

        return url
    except:
        return

