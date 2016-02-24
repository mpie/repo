# -*- coding: utf-8 -*-

import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        O = {
            '___': 0,
            '$$$$': "f",
            '__$': 1,
            '$_$_': "a",
            '_$_': 2,
            '$_$$': "b",
            '$$_$': "d",
            '_$$': 3,
            '$$$_': "e",
            '$__': 4,
            '$_$': 5,
            '$$__': "c",
            '$$_': 6,
            '$$$': 7,
            '$___': 8,
            '$__$': 9,
            '$_': "constructor",
            '$$': "return",
            '_$': "o",
            '_': "u",
            '__': "t",
        }


        url = url.replace('/f/', '/embed/')

        html = client.request(url)


        packed_data = re.search('>\s*(eval\s*\(function.*?)\s*</script>', html, re.DOTALL).group(1)

        new_str = re.search("decodeURIComponent\('(.*?)'\)", packed_data).group(1)

        new_str = urllib.unquote(new_str)
        packed_data = re.sub('decodeURIComponent\(.*?\)', "'%s'" % (new_str), packed_data)

        split_str, delim = re.search(',\s*\((.*?)\)\.split\([\'"](.*?)[\'"]\)', packed_data).groups()


        new_split_str = eval(split_str)
        new_split_str = new_split_str.replace(delim, '|')

        packed_data = re.sub(',\s*\(.*?\)\.split\(.*?\)', ", '%s'.split('%s')" % (new_split_str, '|'), packed_data)

        html = jsunpack.unpack(packed_data)

        html = html.replace('\\\\', '\\')

        html = re.search('o\.\$\(o\.\$\((.*?)\)\(\)\)\(\);', html)


        s1 = html.group(1)
        s1 = s1.replace(' ', '')
        s1 = s1.replace('(![]+"")', 'false')
        s3 = ''
        for s2 in s1.split('+'):
            if s2.startswith('o.'):
                s3 += str(O[s2[2:]])
            elif '[' in s2 and ']' in s2:
                key = s2[s2.find('[') + 3:-1]
                s3 += s2[O[key]]
            else:
                s3 += s2[1:-1]

        s3 = s3.replace('\\\\', '\\')
        s3 = s3.decode('unicode_escape')
        s3 = s3.replace('\\/', '/')
        s3 = s3.replace('\\\\"', '"')
        s3 = s3.replace('\\"', '"')


        url = re.search('<source.+?src="([^"]+)', s3).group(1)
        return url
    except:
        return


