# -*- coding: utf-8 -*-

import re,urllib,time
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        result = client.request(url, mobile=True, close=False)

        try:
            post = {}
            f = client.parseDOM(result, 'Form', attrs = {'method': 'POST'})[0]
            f = f.replace('"submit"', '"hidden"')
            k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
            for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
            post = urllib.urlencode(post)
        except:
            post=None

        for i in range(0, 10):
            try:
                result = client.request(url, post=post, mobile=True, close=False)
                result = result.replace('\n','')

                result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
                result = jsunpack.unpack(result)

                result = re.compile('sources *: *\[.+?\]').findall(result)[-1]
                result = re.compile('file *: *"(http.+?)"').findall(result)

                url = [i for i in result if not '.m3u8' in i]
                if len(url) > 0: return '%s|Referer=%s' % (url[0], urllib.quote_plus('http://vidzi.tv/nplayer/jwplayer.flash.swf'))
                url = [i for i in result if '.m3u8' in i]
                if len(url) > 0: return url[0]
            except:
                time.sleep(1)
    except:
        return

