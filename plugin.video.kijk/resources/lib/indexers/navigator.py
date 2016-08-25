# -*- coding: utf-8 -*-


import os,sys

from resources.lib.modules import control
from resources.lib.modules import client

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

artPath = control.artPath()
addonFanart = control.addonFanart()

class navigator:
    def __init__(self):
        self.base_link = 'http://upload.kijk.nl'
        self.search_link = '/ajax/kanalen/zoeken/undefined/%s'
        self.static_items = 2

    def root(self):
        r = client.request(self.base_link)
        r = client.parseDOM(r, 'h2', attrs = {'class': 'showcase-heading'})

        counter = 0
        items = []
        for i in r:
            if counter < self.static_items:
                items.append(['', i])
                counter += 1
            else:
                items.append([client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'a', ret='title')[0]])

        for uri, name in items:
            if not uri:
                self.addDirectoryItem(name.lower().capitalize(), 'overview&name=%s' % (name), 'movies.png', 'DefaultMovies.png')
            else:
                self.addDirectoryItem(name, 'category&url=%s' % (uri), 'movies.png', 'DefaultMovies.png')

        self.addDirectoryItem('Zoeken', 'search', 'movies.png', 'DefaultMovies.png')

        self.endDirectory()

    def addDirectoryItem(self, name, query, thumb, icon, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True: cm.append(('Queue item', 'RunPlugin(%s?action=queueItem)' % sysaddon))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self):
        control.directory(syshandle, cacheToDisc=True)


