# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import os,sys,re,json,urllib,urllib2,urlparse,base64,datetime

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

from resources.lib.libraries import trakt
from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import metacache
from resources.lib.libraries import favourites
from resources.lib.libraries import workers
from resources.lib.libraries import views

addonFanart = control.addonFanart()
sysaddon = sys.argv[0]

class thai:
    def __init__(self):
        self.list = []
        self.main_link       = 'http://www.seesantv.com/seesantv_2014/%s'
        self.shows_link      = self.main_link % 'program.php?id=%s'
        self.shows_ajax_link = self.main_link % 'program_ajax3.php?id=%s&page=%s'
        self.episodes_ajax_link = self.main_link % 'change_page_ajax.php?page=%s&program_id=%s'
        self.episodes_link = self.main_link % 'program_detail.php?page=%s&id=%s'
        self.member_id = 196985  # expires 25 aug 2017
        self.view_server_name = 'gm1'  # uk1, uk2, gm1, gm2, us1, us3, us4, as1, as2, jp1, jp2
        self.replace_server = 'gm99'  # uk1, uk2, gm1, gm2, us1, us3, us4, as1, as2, jp1, jp2

    '''
    List all the shows from a specific category
    '''
    def listShows(self, catid, page):
        limatch = []
        url = self.shows_link % (catid)

        try: result = client.request(url)
        except: pass

        pageContent = ''.join(result.splitlines()).replace('\'','"')
        pages = re.compile('id="a_page_(.+?)" href').findall(pageContent)

        if str(page) in pages:
            pageUrl = self.shows_ajax_link % (catid, str(page))
            result = client.request(pageUrl)
            limatch+=re.compile('<figure>(.+?)</a></li>').findall(result)

        for li_content in limatch:
            show = re.compile('<a href=".+?id=(.+?)"><img src="(.+?)" alt="(.+?)" w').findall(li_content)
            #print show
            title = show[0][2].decode('iso-8859-11')
            showid = show[0][0]
            image = show[0][1]
            self.list.append({'name': title, 'showid': showid, 'image': image})

        for show in self.list:
            name = show['name'].encode('utf-8')
            showid = show['showid']
            image = show['image']
            action = 'listEpisodes'
            query = '?action=%s&name=%s&catid=%s&showid=%s&image=%s' % (action, name, catid, showid, image)
            url = '%s%s' % (sysaddon, query)
            item = control.item(name, iconImage=image, thumbnailImage=image)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            item.setInfo(type="Video", infoLabels={"Title": name, "OriginalTitle": name})
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        nextPage = int(page) + 1
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
                pageNumber = int(page) + 1
                query = '?action=%s&page=%d&name=%s&catid=%s' % (action, int(page), 'Page ' + str(pageNumber), catid)
                url = '%s%s' % (sysaddon, query)
                item = control.item('Page ' + str(pageNumber), iconImage='', thumbnailImage='')
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                item.setInfo(type="Video", infoLabels={"Title": 'Page ' + str(pageNumber), "OriginalTitle": 'Page ' + str(pageNumber)})
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        control.content(int(sys.argv[1]), 'movies')
        if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(500)')
        control.directory(int(sys.argv[1]), cacheToDisc=True)

    '''
    List all shows episodes
    Page starts at 0
    '''
    def listEpisodes(self, catid, showid, page, image):
        url = self.episodes_link % (page, showid)
        try: result = client.request(url)
        except: pass
        link = ''.join(result.splitlines()).replace('\'','"')
        link = ''.join(link.splitlines()).replace('<i class="icon-new"></i>','')

        episodematch = re.compile('<table class="program-archive">(.+?)</table>').findall(link)
        episodes = re.compile('<a href="(.+?)" >(.+?)</a>.+?</td>\t\t\t\t\t\t\t<td> \t\t\t\t\t\t\t\t<a href="(.+?)" ><img').findall(episodematch[0])

        programMeta = re.compile('<div class="program-meta">(.+?)</div>').findall(link)
        image = re.compile('<img src="(.+?)" alt').findall(programMeta[0])[0]

        # episodes per page
        for episode in episodes:
            name = episode[1].decode('iso-8859-11')
            u = 'http://www.seesantv.com/seesantv_2014/' + episode[0] + '&bitrate=high'
            self.list.append({'name': name, 'url': urllib.quote_plus(u), 'image': image})

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
        paginator = re.compile('<div class="page_list"  align="center">(.+?)</ul>').findall(link)[0]
        pages = re.compile('>(\d+)</a>').findall(paginator)
        nextPage = int(page) + 1
        if nextPage < len(pages):
            action = 'listEpisodes'
            query = '?action=%s&page=%d&name=%s&catid=%s&showid=%s&image=%s' % (action, nextPage, 'Next Page', catid, showid, image)
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
        cookie = 'view_server_name=%s; member_id=%d' % (self.view_server_name, self.member_id)

        try: result = client.request(url, cookie=cookie)
        except: pass

        videoUrl = re.compile('file: "(.+?)"').findall(result)[0]
        videoUrl = videoUrl.replace('us88', self.replace_server)
        videoUrl = videoUrl.replace('http://.', 'http://' + self.replace_server + '.seesantv.com')

        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo(type='Video', infoLabels={'title': name})
        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')
        control.playlist.clear()

        try:
            connection = urllib2.urlopen(videoUrl)
            connection.close()
        except urllib2.HTTPError, e:
            videoUrl = videoUrl.replace('gm99', 'uk88')
            try:
                connection = urllib2.urlopen(videoUrl)
                connection.close()
            except urllib2.HTTPError, e:
                videoUrl = videoUrl.replace('uk88', 'as88')

        control.player.play(videoUrl + '|Referer:' + url, item)
