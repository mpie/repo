# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2016 Mpie

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os, sys, urlparse, re, json

from resources.lib.libraries import client
from resources.lib.libraries import views
from resources.lib.libraries import control

artPath = control.artPath()
addonFanart = control.addonFanart()
sysaddon = sys.argv[0]

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

class livetv:
    def __init__(self):
        self.list = []
        self.host = 'http://urhd.tv/'
        self.url = 'http://urhd.tv/%s'

    def makelist(self):
        html = client.request(self.host)
        html = client.replaceHTMLCodes(html)

        items = re.findall('channels="(\[.+?\])"', html)[0]
        items = json.loads(items)
        for i in items:
            if i['alive']:
                name = i['display_name'].replace('_', ' ').replace('-', ' ')
                link = self.url % (i['slug'])
                url = 'watchLiveTV&url=%s&name=%s' % (link, name)
                print name
                print url
                self.addDirectoryItem(name, url, 'root_livetv.png', 'DefaultMovies.png')
        self.endDirectory()
        views.setView('movies', {'skin.confluence': 50})

    def watchLiveTV(self, name, url):
        page = url + '/embed'
        expres = "file: '(.+token.+?)',"

        html = client.request(page, referer=url)
        url = re.findall(expres, html)[0]

        item = control.item(path=url, iconImage='', thumbnailImage='')
        item.setInfo(type='Video', infoLabels = {'title': name})
        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')
        control.playlist.clear()
        control.player.play(url, item)

    def addDirectoryItem(self, name, query, thumb, icon, context=None, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
        item.addContextMenuItems(cm, replaceItems=False)
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self, cacheToDisc=True):
        control.directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)