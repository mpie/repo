# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import json, re, urllib
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, sys, os

from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import views
from resources.lib.modules import player

addonFanart = control.addonFanart()
syshandle = int(sys.argv[1])
sysaddon = sys.argv[0]


class dutchtv:
    def __init__(self):
        self.baseUrl = 'https://api.kijk.nl/v1/default/sections/%s'
        self.mainList = 'programs-abc-0123456789abcdefghijklmnopqrstuvwxyz?limit=350&offset=0'
        self.showUri = '%s-%s_Episodes-season-0?limit=100&offset=0'
        self.embedUri = 'https://embed.kijk.nl/api/video/%s?id=kijkapp&format=DASH&drm=CENC'
        self.oldEmbedUri = 'https://embed.kijk.nl/video/%s'
        self.bcPlaybackUrl = 'https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s'
        self.User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

    def addDir(self, name, info, u, action, image, isFolder=True):
        url = (sysaddon + "?url=" + urllib.quote_plus(u) + "&name=" + urllib.quote_plus(name.encode('utf-8')) + "&action=" + action + "&image=" + image)

        item = control.item(label=name.encode('utf-8'))
        item.setArt({'icon': image, 'thumb': image})
        item.setInfo(type="Video", infoLabels={"Title": name.encode('utf-8'), "OriginalTitle": name.encode('utf-8'), "Plot": info})

        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def index(self):
        url = self.baseUrl % (self.mainList)
        html = client.request(url)
        data = json.loads(html)
        sortedData = sorted(data['items'], key=lambda d: d['title'])

        for item in sortedData:
            url = self.baseUrl % (self.showUri % (item['type'], item['id']))
            if 'retina_image' in item['images']:
                icon = item['images']['retina_image']
            else:
                icon = item['images']['nonretina_image']

            if 'synopsis' in item:
                info = item['synopsis']
            else:
                info = 'N/A'

            self.addDir(item['title'], info, url, 'listDutchShow', icon)

        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.estuary': control.getSkin(control.setting('tvshows.viewtype')), 'skin.confluence': 500})

    def list(self, url):
        html = client.request(url)
        data = json.loads(html)
        sortedData = sorted(data['items'], key=lambda d: int(d['episode']), reverse=True)

        for item in sortedData:
            url = self.embedUri % (item['id'])
            if 'retina_image' in item['images']:
                icon = item['images']['retina_image']
            else:
                icon = item['images']['nonretina_image']

            if 'synopsis' in item:
                info = item['synopsis']
            else:
                info = 'N/A'

            self.addDir(item['seriesTitle'], info, url, 'playDutchShow', icon, False)

        control.content(syshandle, 'episodes')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('episodes', {'skin.estuary': 55, 'skin.confluence': 50})

    def play(self, name, url, image):
        html = client.request(url)
        data = json.loads(html)

        m3u8Url = data['playlist']

        if m3u8Url != "https://embed.kijk.nl/api/playlist/.m3u8":
            player.player().playLiveStream(name, data['playlist'], image)
            return

        # Try an older player
        videoId = data['vpakey']
        referer = self.oldEmbedUri % (videoId)
        mpdManifestUrl = referer + "?width=868&height=491"

        data = client.request(mpdManifestUrl, referer=referer)
        # First try to find an M3u8
        m3u8Urls = re.compile('https:[^"]+.m3u8', re.DOTALL).findall(data)
        for m3u8Url in m3u8Urls:
            player.player().playLiveStream(name, m3u8Url, image)
            return

        # Maybe the new bc player
        videoId = client.parseDOM(data, 'video', ret='data-video-id')[0]
        accountId = client.parseDOM(data, 'video', ret='data-account')[0]

        brightCoveUrl = self.bcPlaybackUrl % (accountId, videoId)
        print brightCoveUrl
        headers = {'Accept': 'application/json;pk=BCpkADawqM3ve1c3k3HcmzaxBvD8lXCl89K7XEHiKutxZArg2c5RhwJHJANOwPwS_4o7UsC4RhIzXG8Y69mrwKCPlRkIxNgPQVY9qG78SJ1TJop4JoDDcgdsNrg', 'DNT': 1, 'Origin': 'https://embed.kijk.nl', 'User-Agent': self.User_Agent}
        html = client.request(brightCoveUrl, XHR=True, headers=headers, referer=referer)
        data = json.loads(html)

        streams = filter(lambda d: d["container"] == "M2TS", data["sources"])
        if streams:
            streamUrl = streams[0]["src"]
            player.player().playLiveStream(name, streamUrl, image)
            return

        # If all else fails. try the first one with a src
        for item in data['sources']:
            if 'src' in item:
                player.player().playLiveStream(name, item['src'], image)
                return


