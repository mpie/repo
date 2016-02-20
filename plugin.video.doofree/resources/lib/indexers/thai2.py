# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2016 Mpie
'''


import os,sys,re,json,urllib,urlparse,cookielib,urllib2

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
        self.episodes_link   = 'http://www.dootv.com/ajax/mediaItemRow_json_ajax.php?media_id=%s'
        self.stream_link_sd1     = 'http://01-0115-03.thaimediaserver.com/streaming/21ca59dbdf10c176696b54f69b292bf0/56c7b7cc%s'
        self.stream_link_sd2     = 'http://edge4-04.thaimediaserver.com/%s/_definst_/vod%s'
        self.stream_link_hd     = 'http://edge6-09.thaimediaserver.com/%s/_definst_/vod/HD%s'
        self.player_link     = self.main_link % 'player/?media_id=%d&customers_id=137288&media_item_id=%d&HD=1&server=EU'

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
        url = self.episodes_link % (showid)
        try: result = client.request(url)
        except: pass
        result = re.compile('(.+?)]').findall(result)[0] + ']'
        shows = json.loads(result)

        # episodes per page
        for show in shows:
            if 'Not Show' == show['item_title']:
                continue
            name = show['media_title'] + ' ' + show['item_title']
            u = self.player_link % (show['media_id'], show['media_item_id'])

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

        control.content(int(sys.argv[1]), 'movies')
        if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(50)')
        control.directory(int(sys.argv[1]), cacheToDisc=True)

    '''
    Get the video url by member_id cookie
    Start playing the video
    '''
    def sourcePage(self, url, name, image):
        print url

        username = 'b359980@trbvn.com'
        password = 'rinus123'

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        login_data = urllib.urlencode({'email' : username, 'password' : password, 'remember' : 'false'})
        opener.open('http://service.thaiflix.com/api/v1/auth/login', login_data)
        resp = opener.open(url)
        data = json.loads(resp.read())

        if 'url2' in data['file']:
            location = data['file']['url2']
        else:
            location = data['file']['url1']

        item = control.item(iconImage=image, thumbnailImage=image)
        item.setInfo( type='Video', infoLabels = {'title': name} )
        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')
        control.playlist.clear()
        control.player.play(location, item)
