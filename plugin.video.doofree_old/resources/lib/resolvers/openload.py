# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries.aa_decoder import AADecoder


def resolve(url):
    def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
        return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

    def conv(s, addfactor=None):
        if 'function()' in s:
            addfactor = s.split('b.toString(')[1].split(')')[0]
            fname = re.findall('function\(\)\{function (.*?)\(', s)[0]
            s = s.replace(fname, 'myfunc')
            s = ''.join(s.split('}')[1:])
        if '+' not in s:
            if '.0.toString' in s:
                ival, b = s.split('.0.toString(')
                b = b.replace(')', '')
                return baseN(int(ival), int(eval(b)))
            elif 'myfunc' in s:
                b, ival = s.split('myfunc(')[1].split(',')
                ival = ival.replace(')', '').replace('(', '')
                b = b.replace(')', '').replace('(', '')
                b = eval(addfactor.replace('a', b))
                return baseN(int(ival), int(b))
            else:
                return eval(s)
        r = ''
        for ss in s.split('+'):
            r += conv(ss, addfactor)
        return r

    try:
        html = client.request(url)
        aaencoded = re.findall('id=\"olvideo\".*\n.*?text/javascript\">(.*)</script>', html)[0]
        dtext = AADecoder(aaencoded).decode()
        dtext = re.findall('window.vs=(.*?);', dtext)[0]
        dtext = conv(dtext)
        url = dtext.replace("https", "http")

        return url
    except:
        return

