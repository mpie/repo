# -*- coding: utf-8 -*-

import re,urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        channel = urlparse.urlparse(url).path
        channel = re.compile('/([\w]+)').findall(channel)[-1]
        domain = urlparse.urlparse(url).netloc


        pageUrl = urlparse.urljoin('http://%s' % domain, channel)

        if 'instagib' in domain: playpath = 'instagib_%s' % channel
        elif 'breakers' in domain: playpath = 'btv_%s' % channel
        elif 'vapers' in domain: playpath = 'vtv_%s' % channel
        else: playpath = 'live_%s' % channel


        result = client.request(pageUrl, referer=pageUrl)

        swfUrl = re.compile('"(/\d+/swf/[0-9A-Za-z]+\.swf)').findall(result)[0]
        swfUrl = urlparse.urljoin(pageUrl, swfUrl)


        infoUrl = 'http://mvn.vaughnsoft.net/video/edge/%s_%s' % (domain, channel)
        result = client.request(infoUrl)

        streamer = re.compile('(.+?);').findall(result)[0]
        streamer = 'rtmp://%s/live' % streamer

        app = re.compile('mvnkey-(.+)').findall(result)[0]
        app = 'live?%s' % app

        url = '%s app=%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true live=true timeout=20' % (streamer, app, playpath, pageUrl, swfUrl)

        return url
    except:
        return

