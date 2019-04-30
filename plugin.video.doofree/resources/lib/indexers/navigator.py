# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 DooFree

'''


import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import views
from resources.lib.modules import client


sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; control.moderator()

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    def root(self):
        self.addDirectoryItem(32001, 'movieNavigator', 'root_movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'root_series.png', 'DefaultTVShows.png')

        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')

        self.addDirectoryItem('Dutch TV Shows', 'dutchTV', 'DefaultMovies.png', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Live TV', 'thaiLiveTV', 'root_thaitv.png', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Shows', 'thaiShows', 'root_thaishows.png', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Shows 2', 'thaiShows2', 'root_thaishows2.png', 'DefaultMovies.png')
        self.addDirectoryItem('Hindi movies', 'bollywood', 'root_hindimovies.png', 'DefaultMovies.png')
        self.addDirectoryItem('Cartoon', 'cartoons', 'root_cartoon.png', 'DefaultMovies.png')
        self.addDirectoryItem('Cleanup', 'clearSources', 'root_cleanup.png', 'DefaultAddonProgram.png')
        self.endDirectory()
        views.setView('movies', {'skin.estuary': 500, 'skin.confluence': 500})


    def thaiLiveTV(self):
        self.addDirectoryItem('ONE',
                              'playThaiLiveTV&url=http://live1.thaimomo.com/live/chone1/playlist.m3u8&name=ONE_HD&image=ch1hd.png',
                              'ch1hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('3HD',
                              'playThaiLiveTV&url=http://live3.thaimomo.com/live/ch3hd3b/playlist.m3u8&name=3HD&image=ch3hd.png',
                              'ch3hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('3SD', 'playThaiLiveTV&url=http://live3.thaimomo.com/live/ch3SD1/playlist.m3u8',
                              'ch3sd.png',
                              'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('3Family',
                              'playThaiLiveTV&url=http://live1.thaimomo.com/live/ch3family1/playlist.m3u8&name=3Family&image=ch3family.png',
                              'ch3family.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('5HD',
                              'playThaiLiveTV&url=http://live1.thaimomo.com/live/ch5hd1/playlist.m3u8&name=5HD&image=ch5hd.png',
                              'ch5hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('7HD',
                              'playThaiLiveTV&url=http://live1.thaimomo.com/live/ch7hd1/playlist.m3u8&name=7HD&image=ch7hd.png',
                              'ch7hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('8HD',
                              'playThaiLiveTV&url=http://live1.thaimomo.com/live/cheight1/playlist.m3u8&name=8HD&image=ch8hd.png',
                              'ch8hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('WorkPoint',
                              'playThaiLiveTV&url=http://live1.thaimomo.com/live/chworkpoint1/playlist.m3u8&name=WORKPOINT&image=chworkpoint.png',
                              'chworkpoint.png', 'DefaultMovies.png', isFolder=False)
        self.endDirectory()


    def thaiShows(self):
        self.addDirectoryItem('ละครไทย (ออนแอร์) / Thai Dramas (on air)', 'listShows&catid=18&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('ละครไทย (อวสาน) / Thai Dramas (ended)', 'listShows&catid=27&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('ซีรี่ย์เกาหลี / Korean Series', 'listShows&catid=17&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('หนังจีนชุด / Chinese Series', 'listShows&catid=37&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('รายการอาหาร / Cooking Shows', 'listShows&catid=15&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('วาไรตี้โชว์ / Variety Shows', 'listShows&catid=8&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('เรียลลิตี้โชว์ / Reality & Singing Contest', 'listShows&catid=84&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('เกมส์โชว์ / Game Shows', 'listShows&catid=2&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('ข่าว / Thai News', 'listShows&catid=4&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('ทอล์กโชว์ / Talk Shows', 'listShows&catid=3&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('ภาพยนตร์ไทย / Thai Movies', 'listShows&catid=92&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('ภาพยนตร์ฝรั่งใหม่ / US Movies (Thai dubbed)', 'listShows&catid=98&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('ซีรี่ย์ฝรั่ง / US Series (Thai dubbed)', 'listShows&catid=38&page=1', '', 'DefaultMovies.png')
        self.addDirectoryItem('ภาพยนตร์แอนนิเมชั่น / Animation', 'listShows&catid=93&page=1', '', 'DefaultMovies.png')
        self.endDirectory()


    def thaiShows2(self):
        self.addDirectoryItem('Thai Drama (on air)', 'listShows2&catid=8&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('K-J Series', 'listShows2&catid=10&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('C-T Series', 'listShows2&catid=11&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('K-J Series (Thai Dub)', 'listShows2&catid=41&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Breaking News', 'listShows2&catid=19&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Entertainment News', 'listShows2&catid=20&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('News Analysis', 'listShows2&catid=21&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Talk Show', 'listShows2&catid=24&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Variety Show', 'listShows2&catid=25&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Game - Quiz', 'listShows2&catid=26&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Food - Health', 'listShows2&catid=27&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Sport', 'listShows2&catid=28&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Travel', 'listShows2&catid=29&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Doumentary', 'listShows2&catid=30&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Movies', 'listShows2&catid=12&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Movies Classic', 'listShows2&catid=50&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Chinese Movies', 'listShows2&catid=51&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Korean Movies', 'listShows2&catid=52&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Japanese Movies', 'listShows2&catid=53&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Indian Movies', 'listShows2&catid=54&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Other Movies', 'listShows2&catid=55&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Sitcoms', 'listShows2&catid=22&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Comedy', 'listShows2&catid=23&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Music TV', 'listShows2&catid=14&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Singing Contest', 'listShows2&catid=15&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Concert', 'listShows2&catid=16&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Local Theater', 'listShows2&catid=17&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Karaoke', 'listShows2&catid=18&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Cartoon (on air)', 'listShows2&catid=64&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Cartoon Sports', 'listShows2&catid=65&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Cartoon Action/Adventure', 'listShows2&catid=66&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Girl Cartoon', 'listShows2&catid=67&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Cartoon Investigation', 'listShows2&catid=68&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Other Cartoon', 'listShows2&catid=69&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Contest', 'listShows2&catid=31&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Study Languages', 'listShows2&catid=32&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Kid', 'listShows2&catid=33&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Dhamma', 'listShows2&catid=34&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Special Show', 'listShows2&catid=35&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('18+', 'listShows2&catid=36&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32005, 'movies&url=featured', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def bollywood(self):
        url = 'http://www.join4films.com'
        html = client.request(url)

        r = client.parseDOM(html, 'ul', attrs={'class': 'sub-menu'})
        r = client.parseDOM(r, 'li')
        url = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
        url = [(i[0][0], i[1][0]) for i in url if len(i[0]) > 0 and len(i[1]) > 0]

        del url[-2:]
        for i in url:
            link = i[0]
            title = i[1]
            self.addDirectoryItem(title, 'listBollywood&url=%s&page=%d' % (link, 1), 'DefaultMovies.jpg', 'DefaultMovies.png')

        self.endDirectory()


    def views(self):
        try:
            control.idle()

            items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1: return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import cache
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()


    def infoCheck(self, version):
        try:
            control.infoDialog('DooFree', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


