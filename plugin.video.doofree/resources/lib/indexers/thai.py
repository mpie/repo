# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import os,sys,re,json,urllib,urllib2,urlparse,base64,datetime,requests

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import views

addonFanart = control.addonFanart()
sysaddon = sys.argv[0]

class thai:
    def __init__(self):
        self.list = []
        self.img1            = 'https://seesantv.com/'
        self.img2            = 'https://www.seesantv.com/seesantv2020/file_management/images/programs'
        self.main_link       = 'https://seesantv.com/seesantv2020/%s'
        self.login_link      = self.main_link % 'apps/index.php?module=members&task=checkLogin'
        self.shows_link      = self.main_link % 'apps/index.php?module=programs&task=setLoadListTypeAll&category=%s&page=%s'
        self.episodes_link = self.main_link % 'apps/index.php?module=programs&task=setLoadChapterListByPages2020&program_id=%s&page=%s'
        self.player_link = self.main_link % 'player-%s'
        self.member_id = 217290
        self.view_server_id = 403 # 405 = gm, 403 = uk
        self.replace_server = 'gm99'  # uk1, uk2, gm1, gm2, us1, us3, us4, as1, as2, jp1, jp2
        self.User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

    '''
    List all the shows from a specific category
    '''
    def listShows(self, catid, page):
        syshandle = int(sys.argv[1])
        limatch = []
        url = self.shows_link % (catid, page)
        try: result = client.request(url)
        except: pass

        data = json.loads(result)
        pageContent = data['content'].encode('utf-8')

        # todo: fix pagination
        pages = range(2, 6)

        limatch += re.compile('<figure>(.+?)</a></li>').findall(pageContent)

        for li_content in limatch:
            show = re.compile('program-(.+?)" target.+?src="(.+?)".+?h5>(.+?)</h5').findall(li_content)
            title = show[0][2].decode('utf-8')
            showid = show[0][0]
            image = show[0][1]

            if 'program_pic/program_' in image:
                image = image.replace('../', self.img1)
            else:
                image = image.replace('../', self.img2)
                image = image.replace('program_pic', '')

            self.list.append({'name': title, 'showid': showid, 'image': image})

        for show in self.list:
            name = show['name'].encode('utf-8')
            showid = show['showid']
            image = show['image']
            action = 'listEpisodes'
            query = '?action=%s&name=%s&catid=%s&showid=%s&image=%s&page=1' % (action, name, catid, showid, image)
            url = '%s%s' % (sysaddon, query)
            item = control.item(name, iconImage=image, thumbnailImage=image)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        nextPage = int(page)
        if nextPage <= len(pages):
            if 'first' in pages:
                pages.remove('first')
            if 'pre' in pages:
                pages.remove('pre')
            if 'next' in pages:
                pages.remove('next')
            if 'last' in pages:
                pages.remove('last')

            for page in pages:
                action = 'listShows'
                pageNumber = int(page)
                query = '?action=%s&page=%d&name=%s&catid=%s' % (action, int(page), 'Page ' + str(pageNumber), catid)
                url = '%s%s' % (sysaddon, query)
                item = control.item('Page ' + str(pageNumber), iconImage='', thumbnailImage='')
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                item.setInfo(type="Video", infoLabels={"Title": 'Page ' + str(pageNumber), "OriginalTitle": 'Page ' + str(pageNumber)})
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)

        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.estuary': 500, 'skin.confluence': 500})

    '''
    List all shows episodes
    Page starts at 0
    '''
    def listEpisodes(self, catid, showid, page, image):
        syshandle = int(sys.argv[1])
        url = self.episodes_link % (showid, page)
        cookie = 'ssMemberID=%d' % (self.member_id)
        try: result = client.request(url, cookie=cookie)
        except: pass

        print url
        data = json.loads(result)
        r = client.parseDOM(data['list'].encode('utf-8'), 'li')
        episodes = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]

        for episode in episodes:
            name = re.compile('<i class="fas fa-play-circle-player "></i> (.+)').findall(episode[1][0].encode('utf-8'))[0]
            url = episode[0][0]
            self.list.append({'name': name, 'url': urllib.quote_plus(url), 'image': image})

        for episode in self.list:
            name = episode['name']
            url = episode['url']
            image = episode['image']
            action = 'sourcePage'
            query = '?action=%s&image=%s&url=%s&name=%s' % (action, image, url, urllib.quote_plus(name))

            url = '%s%s' % (sysaddon, query)
            item = control.item(name, iconImage=image, thumbnailImage=image)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)

        # Check if we need next/prev page link
        last_item = self.list[-1]
        episode_number = re.findall(r'\d+', last_item['name'])[-1]
        show_next_page = int(episode_number) > 1
        show_prev_page = int(page) > 1

        if show_next_page:
            name = 'Next page'
            item = control.item(name, iconImage='', thumbnailImage='')
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            query = '?action=listEpisodes&name=%s&catid=%s&showid=%s&image=''&page=%d' % (name, catid, showid, int(page) + 1)
            url = '%s%s' % (sysaddon, query)
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        if show_prev_page:
            name = 'Previous page'
            item = control.item(name, iconImage='', thumbnailImage='')
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            query = '?action=listEpisodes&name=%s&catid=%s&showid=%s&image=''&page=%d' % (name, catid, showid, int(page) - 1)
            url = '%s%s' % (sysaddon, query)
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        control.content(syshandle, 'episodes')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('episodes', {'skin.estuary': 55, 'skin.confluence': 50})

    '''
    Get the video url by member_id cookie
    Start playing the video
    '''
    def sourcePage(self, url, name, image):
        response = urllib.urlopen('http://api.ipstack.com/check?access_key=527d4ea99987d55558c10b3a7d6c7b9b')
        data = json.loads(response.read())

        if (data['country_code'] == 'TH'):
            viewServerId = 409
        else:
            viewServerId = self.view_server_id

        cookie = 'ssCheckLogin2=1; viewServersID=%d; ssMemberID=%d; ssMemberUsername=%s; ssMemberPassword=%s' % (viewServerId, self.member_id, 'endy.adorian%40niickel.us', 'test12345')
        headers = {'Host': 'www.seesantv.com', 'Referer': url, 'User-Agent': self.User_Agent}

        try: result = client.request(url, cookie=cookie, headers=headers)
        except: pass

        vidFile = re.compile('file: "(.+?)"').findall(result)[0]
        videoUrl = vidFile.replace('s.mp4', '.mp4')

        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo(type='Video', infoLabels={'title': name})
        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')
        control.playlist.clear()

        control.player.play(videoUrl + '|Referer:' + url, item)
