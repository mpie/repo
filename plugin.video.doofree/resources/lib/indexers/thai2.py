# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2016 Mpie
'''


import os,sys,re,json,urllib,urlparse,base64,datetime

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

from resources.lib.libraries import control
from resources.lib.libraries import client

addonFanart = control.addonFanart()
sysaddon = sys.argv[0]

class thai:
    def __init__(self):
        self.list = []
        self.main_link       = 'http://service.thaiflix.com/api/v1/%s'
        self.cdn             = 'http://cdn.thaiflix.com/media/files/images-large/%s'
        self.shows_link      = self.main_link % 'medias/newest?page=%s&pageLimit=%s&channel_id=%s&category_id=%s'
        self.episodes_link   = self.main_link % 'medias/%s/media-items?page=%s'
        #self.stream_link     = 'http://edge4-07.thaimediaserver.com/AsianSeries16/_definst_/vod/'
        self.stream_link     = 'http://edge4-02.thaimediaserver.com/AsianSeries16/_definst_/vod/'

    '''
    List all the shows from a specific category
    '''
    def listShows(self, catid, page, limit, channel):
        url = self.shows_link % (page, limit, channel, catid)
        try: result = client.request(url)
        except: pass

        data = json.loads(result)
        paginationInfo = data['pagination']
        shows = data['data']

        for show in shows:
            title = show['media_title']
            showid = show['media_id']
            image = self.cdn % (show['image_file'])
            self.list.append({'name': title, 'showid': showid, 'image': image})

        for show in self.list:
            name = show['name']
            showid = show['showid']
            image = show['image']
            action = 'listEpisodes2'
            query = '?action=%s&name=%s&showid=%s&image=%s&page=1' % (action, name, showid, image)
            url = '%s%s' % (sysaddon, query)
            item = control.item(name, iconImage=image, thumbnailImage=image)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        nextPage = int(page) + 1
        if nextPage <= paginationInfo['totalPages']:
            for page in range(1, paginationInfo['totalPages']):
                action = 'listShows2'
                query = '?action=%s&page=%d&name=%s&catid=%s&limit=%s&channel=%s' % (action, page, 'Page ' + str(page), catid, limit, channel)
                url = '%s%s' % (sysaddon, query)
                item = control.item('Page ' + str(page), iconImage='', thumbnailImage='')
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                item.setInfo(type="Video", infoLabels={"Title": 'Page ' + str(page), "OriginalTitle": 'Page ' + str(page)})
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        control.content(int(sys.argv[1]), 'movies')
        if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(500)')
        control.directory(int(sys.argv[1]), cacheToDisc=True)

    '''
    List all shows episodes
    Page starts at 0
    '''
    def listEpisodes(self, showid, page, image):
        '''
        u='HD/AsianSeries16/160112-UnemployedRomance/UnemployedRomance-Disc4-(15-Jan-2016)_HD.mp4/playlist.m3u8'
        item = control.item(path='', iconImage=image, thumbnailImage=image)
        item.setInfo( type='Video', infoLabels = {'title': 'bla'} )
        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')
        control.playlist.clear()
        control.player.play(u, item)
        return
        url = self.episodes_link % (showid, page)
        print url
        return
        '''
        url = self.episodes_link % (showid, page)
        try: result = client.request(url)
        except: pass

        print result
        return
        data = json.loads(result)
        paginationInfo = data['pagination']
        shows = data['data']

        # episodes per page
        for show in shows:
            name = show['title_en']
            u = self.stream_link % (show['media_id'], show['media_item_id'])
            self.list.append({'name': name, 'url': urllib.quote_plus(u), 'image': image})

        for episode in self.list:
            name = episode['name']
            url = episode['url']
            image = episode['image']
            action = 'sourcePage2'
            query = '?action=%s&image=%s&url=%s&name=%s' % (action, image, url, name)

            url = '%s%s' % (sysaddon, query)
            item = control.item(name, iconImage=image, thumbnailImage=image)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)

        # Pagination
        nextPage = int(page) + 1
        if nextPage <= paginationInfo['totalPages']:
            action = 'listEpisodes2'
            query = '?action=%s&page=%d&name=%s&showid=%s&image=%s' % (action, nextPage, 'Next Page', showid, image)
            url = '%s%s' % (sysaddon, query)
            item = control.item('Next Page', iconImage=image, thumbnailImage=image)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            item.setInfo(type="Video", infoLabels={"Title": 'Next Page', "OriginalTitle": 'Next Page'})
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        control.content(int(sys.argv[1]), 'movies')
        if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(50)')
        control.directory(int(sys.argv[1]), cacheToDisc=True)

    '''
    Get the video url by member_id cookie
    Start playing the video
    '''
    def sourcePage(self, url, name, image):
        cookie = 'member_id=%d;view_server_name=%s' % (self.member_id, self.view_server_name)
        try: result = client.request(url, cookie=cookie)
        except: pass

        videoUrl = re.compile('file: "(.+?)"').findall(result)
        print videoUrl
        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type='Video', infoLabels = {'title': name} )
        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')
        control.playlist.clear()
        control.player.play(videoUrl[0], item)
