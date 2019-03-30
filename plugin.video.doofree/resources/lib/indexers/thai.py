# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import os,sys,re,json,urllib,urllib2,urlparse,base64,datetime

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
        self.img2            = 'http://www.seesantv.com/seesantv2017/file_management/images/programs'
        self.main_link       = 'http://www.seesantv.com/seesantv2017/%s'
        self.shows_link      = self.main_link % 'apps/index.php?module=programs&task=setLoadListTypeAll&category=%s&page=%s'
        #self.shows_ajax_link = self.main_link % 'apps/index.php?module=programs&task=setLoadListTypeAll&category=%s&page=%s&all_page=%s'
        #self.episodes_ajax_link = self.main_link % 'apps/index.php?module=programs&task=setLoadListTypeAll&category=%s'
        self.episodes_link = self.main_link % 'program-%s&datapage=%s'
        self.player_link = self.main_link % 'player-%s'
        self.member_id = 169754  # expires 15 jun 2019
        self.view_server_id = 400
        self.replace_server = 'gm99'  # uk1, uk2, gm1, gm2, us1, us3, us4, as1, as2, jp1, jp2

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
        link = ''.join(result.splitlines()).replace('\'','"')
        link = ''.join(link.splitlines()).replace('<i class="fa fa-play-circle-white"></i>','')

        episodematch = re.compile('class="chapterList">(.+?)</li>').findall(link)

        for em in episodematch:
            episodes = re.compile('player-(.+)">(.+)</a>').findall(em)
            for episode in episodes:
                name = episode[1].decode('utf-8')
                url = self.player_link % (episode[0])
                self.list.append({'name': name, 'url': urllib.quote_plus(url), 'image': image})

        for episode in self.list:
            name = episode['name'].encode('utf-8')
            url = episode['url']
            image = episode['image']
            action = 'sourcePage'
            query = '?action=%s&image=%s&url=%s&name=%s' % (action, image, url, urllib.quote_plus(name))

            url = '%s%s' % (sysaddon, query)
            item = control.item(name, iconImage=image, thumbnailImage=image)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)

        # Pagination
        # paginator = re.compile('<div class="page_list"  align="center">(.+?)</ul>').findall(link)[0]
        # pages = re.compile('>(\d+)</a>').findall(paginator)
        # nextPage = int(page) + 1
        # if nextPage < len(pages):
        #     action = 'listEpisodes'
        #     query = '?action=%s&page=%d&name=%s&catid=%s&showid=%s&image=%s' % (action, nextPage, 'Next Page', catid, showid, image)
        #     url = '%s%s' % (sysaddon, query)
        #     item = control.item('Next Page', iconImage=image, thumbnailImage=image)
        #     if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        #     item.setInfo(type="Video", infoLabels={"Title": 'Next Page', "OriginalTitle": 'Next Page'})
        #     control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)

        control.content(syshandle, 'episodes')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('episodes', {'skin.estuary': 55, 'skin.confluence': 50})

    '''
    Get the video url by member_id cookie
    Start playing the video
    '''
    def sourcePage(self, url, name, image):
        response = urllib.urlopen('http://api.ipstack.com/check?access_key=527d4ea99987d55558c10b3a7d6c7b9b');
        data = json.loads(response.read())

        if (data['country_code'] == 'TH'):
            viewServerId = 409
        else:
            viewServerId = self.view_server_id

        cookie = 'viewLivePlatform=%s; viewEmbedServersID=%d; viewServersID=%d; ssMemberID=%d' % ('pc', viewServerId, viewServerId, self.member_id)

        try: result = client.request(url, cookie=cookie)
        except: pass

        vidFile = re.compile('file: "(.+?)"').findall(result)[0]
        videoUrl = vidFile.replace('s.mp4', '.mp4')

        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo(type='Video', infoLabels={'title': name})
        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')
        control.playlist.clear()

        control.player.play(videoUrl + '|Referer:' + url, item)
