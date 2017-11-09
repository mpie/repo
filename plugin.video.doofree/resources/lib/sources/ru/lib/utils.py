# -*- coding: utf-8 -*-

"""
    DooFree Add-on
    Copyright (C) 2017 Mpie
"""


def uni2cp(ustr):
    raw = ''
    uni = unicode(ustr, 'utf8')
    uni_sz = len(uni)
    for i in range(uni_sz):
        raw += '%%%02X' % ord(uni[i].encode('cp1251'))
    return raw
