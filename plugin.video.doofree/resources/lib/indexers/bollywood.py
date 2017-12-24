# -*- coding: utf-8 -*-


import urlparse,urllib,random,re,os,sys
try: import xbmc
except: pass

from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import views

sysaddon = sys.argv[0]

class bollywood:
    def __init__(self):
        self.host = 'http://www.join4films.com'

    def listBollywood(self, url, page):
        try: html = client.request(url + 'page/' + str(page))
        except: pass

        syshandle = int(sys.argv[1])

        result = client.parseDOM(html, 'article', attrs={'id': 'posts'})
        result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='src'), client.parseDOM(i, 'a')) for i in result]
        result = [(i[0][0], i[1][0], i[2][1]) for i in result if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2][1]) > 0]

        for movie in result:
            uri = movie[0]
            image = movie[1]
            name = movie[2]
            action = 'resolveBollywoodUrl'
            query = '%s?action=%s&name=%s&url=%s&image=%s' % (sysaddon, action, name, uri, image)
            item = control.item(name, iconImage=image, thumbnailImage=image)
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            control.addItem(handle=int(sys.argv[1]), url=query, listitem=item, isFolder=True)

        pageNum = int(page)+1
        query = '%s?action=%s&url=%s&page=%s' % (sysaddon, 'listBollywood', url, pageNum)

        item = control.item('Next page', iconImage='', thumbnailImage='')
        item.setInfo(type="Video", infoLabels={"Title": 'Page ' + str(page), "OriginalTitle": 'Page ' + str(page)})
        control.addItem(handle=syshandle, url=query, listitem=item, isFolder=True)

        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 500, 'skin.confluence': 500})

    def resolveUrl(self, name, url, image):
        try: html = client.request(url)
        except: pass

        video = re.findall('file: "(.+)"', html)[0]

        try:

            label = name
            item = control.item(path=video, iconImage=image, thumbnailImage=image)
            item.setInfo(type='Video', infoLabels={'title': label})
            control.playlist.clear()
            control.player.play(video, item)
        except:
            pass