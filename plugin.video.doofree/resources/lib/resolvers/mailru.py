# -*- coding: utf-8 -*-

import re,json,urllib
import requests


def resolve(url):
    try:
        usr = re.compile('/mail/(.+?)/').findall(url)[0]
        vid = re.compile('(\d*)[.]html').findall(url)[0]
        url = 'http://videoapi.my.mail.ru/videos/mail/%s/_myvideo/%s.json?ver=0.2.60' % (usr, vid)

        result = requests.get(url).content
        cookie = requests.get(url).headers['Set-Cookie']

        u = json.loads(result)['videos']
        h = "|Cookie=%s" % urllib.quote(cookie)

        url = []
        try: url += [[{'quality': '1080p', 'url': i['url'] + h} for i in u if i['key'] == '1080p'][0]]
        except: pass
        try: url += [[{'quality': 'HD', 'url': i['url'] + h} for i in u if i['key'] == '720p'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i['url'] + h} for i in u if not (i['key'] == '1080p' or i ['key'] == '720p')][0]]
        except: pass

        if url == []: return
        return url
    except:
        return

