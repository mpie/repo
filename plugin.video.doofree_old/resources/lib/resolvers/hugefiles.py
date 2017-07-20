# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries import captcha

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36'

def resolve(url):
    try:
        media_id = re.search('//.+?/([\w]+)', url).group(1)
        url = 'http://hugefiles.net/embed-%s.html' % media_id
        result = client.request(url)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })
        f += client.parseDOM(result, 'form', attrs = {'action': '' })
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': 'Free Download'})
        post.update(captcha.request(result))
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        packed = re.search('id="player_code".*?(eval.*?\)\)\))', result, re.DOTALL)

        if packed:
            js = unpack(packed.group(1))
            link = re.search('name="src"0="([^"]+)"/>', js.replace('\\',''))
            if link:
                # print 'HugeFiles Link Found: %s' % link.group(1)
                return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
            else:
                link = re.search("'file','(.+?)'", js.replace('\\',''))
                if link:
                    # print 'HugeFiles Link Found: %s' % link.group(1)
                    return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
    except:
        return

def check(url):
    try:
        result = client.request(url)
        if result == None: return False
        if 'File Not Found' in result: return False
        return True
    except:
        return False

def unpack(sJavascript):
    aSplit = sJavascript.split(";',")
    p = str(aSplit[0])
    aSplit = aSplit[1].split(",")
    a = int(aSplit[0])
    c = int(aSplit[1])
    k = aSplit[2].split(".")[0].replace("'", '').split('|')
    e = ''
    d = ''
    sUnpacked = str(__unpack(p, a, c, k, e, d))
    return sUnpacked.replace('\\', '')

def __unpack(p, a, c, k, e, d):
    while (c > 1):
        c = c -1
        if (k[c]):
            p = re.sub('\\b' + str(__itoa(c, a)) +'\\b', k[c], p)
    return p

def __itoa(num, radix):
    result = ""
    while num > 0:
        result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
        num /= radix
    return result

