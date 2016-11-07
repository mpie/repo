# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2015 Mpie
'''

import xbmc, os, sys, urlparse, json, urllib2, re

from resources.lib.libraries import control
from resources.lib.libraries import views
from resources.lib.libraries import client

artPath = control.artPath()

addonFanart = control.addonFanart()

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

traktMode = False if control.setting('trakt_user') == '' else True

imdbMode = False if control.setting('imdb_user') == '' else True

sysaddon = sys.argv[0]


class navigator:

    def parseJson(self, url):
        req = urllib2.Request(url)
        opener = urllib2.build_opener()
        f = opener.open(req)
        data = json.loads(f.read())
        return data

    def root(self):
        self.addDirectoryItem('Movies', 'movieNavigator', 'root_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem('Series', 'tvNavigator', 'root_shows.jpg', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Live TV', 'thaiLiveTV', 'root_livetv.jpg', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Shows', 'thaiShows', 'root_thai.jpg', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Shows 2', 'thaiShows2', 'root_thai.jpg', 'DefaultMovies.png')
        self.addDirectoryItem('Live TV', 'liveTV', 'root_livetv.png', 'DefaultMovies.png')
        self.addDirectoryItem('Cartoons', 'cartoons', 'cartoons.png', 'DefaultMovies.png')
        self.addDirectoryItem(30119, 'clearSources', 'experiment.jpg', 'DefaultAddonProgram.png')
        #self.addDirectoryItem('1080P Movies', '1080p', 'hd-logo.png', 'DefaultMovies.png')
        #self.addDirectoryItem('Experiment', 'thaiShows2', 'experiment.jpg', 'DefaultMovies.png')
        #self.addDirectoryItem('Working on DooFree 3.0 to make things faster', '', '', 'DefaultMovies.png')
        '''
        if (traktMode == True and not control.setting('tv_alt_widget') == '0') or (traktMode == False and not control.setting('tv_widget') == '0'):
            self.addDirectoryItem(30006, 'tvWidget', 'calendarsAdded.jpg', 'DefaultRecentlyAddedEpisodes.png')
        '''
        self.endDirectory()
        views.setView('movies', {'skin.confluence': 500})

        from resources.lib.libraries import cache
        from resources.lib.libraries import changelog
        cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')

    def thaiLiveTV(self):
        # live4 is asia, uk99 is uk
        self.addDirectoryItem('3HD', 'playThaiLiveTV&url=http://edge4-04.thaimediaserver.com/chlive3/live3stream_720p_20150924/playlist.m3u8&image=ch3hd.png', 'ch3hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('3SD', 'playThaiLiveTV&url=http://edge4-03.thaimediaserver.com/chlive3sd/live3sd_20150924/playlist.m3u8&image=ch3hd.png', 'ch3hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('3Family', 'playThaiLiveTV&url=http://edge4-10.thaimediaserver.com/chlive3family/live3family_20150924/playlist.m3u8&image=ch3hd.png', 'ch3hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('3HD Alternative', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/ch3hd&name=3HD&image=ch3hd.png', 'ch3hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('5', 'playThaiLiveTV&url=http://edge4-04.thaimediaserver.com/chlive5/live5stream_20150924/playlist.m3u8&name=5&image=ch5hd.png', 'ch5hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('5 Alternative', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/ch5hd&name=5HD&image=ch5hd.png', 'ch5hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('7HD', 'playThaiLiveTV&url=http://edge4-09.thaimediaserver.com/chlive7/live7stream_720p_20150924/playlist.m3u8&name=7HD&image=ch7hd.png', 'ch7hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('7HD Alternative', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/ch7hd&name=7HD&image=ch7hd.png', 'ch7hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('8', 'playThaiLiveTV&url=http://edge3-04.thaimediaserver.com/chlive8/live8stream_20150924/playlist.m3u8&name=8HD&image=ch8hd.png', 'ch8hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('8 Alternative', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/cheight1&name=8HD&image=ch8hd.png', 'ch8hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('WorkPoint', 'playThaiLiveTV&url=http://edge7-03.thaimediaserver.com/chliveWorkpoint/liveWorkPointstream_20150924/playlist.m3u8&name=WORKPOINT&image=workpoint.jpg', 'workpoint.jpg', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('WorkPoint Alternative', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/chworkpointHD&name=WORKPOINT_HD&image=workpoint.jpg', 'workpoint.jpg', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('MCOT', 'playThaiLiveTV&url=http://edge4-06.thaimediaserver.com/chlive9/live9stream_20150924/playlist.m3u8&name=MCOT_HD&image=ch9hd.png', 'ch9hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('MCOT Alternative', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/chmcothd&name=MCOT_HD&image=ch9hd.png', 'ch9hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('NBT', 'playThaiLiveTV&url=http://edge4-04.thaimediaserver.com/chliveNBT/liveNBTstream_20150924/playlist.m3u8&name=NBT&image=nbt.png', 'nbt.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('TPBS', 'playThaiLiveTV&url=http://edge4-01.thaimediaserver.com/chliveTPBS/liveTPBSstream_20150924/playlist.m3u8&name=TPBS&image=tbps.png', 'tpbs.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('ONE', 'playThaiLiveTV&url=http://edge4-04.thaimediaserver.com/chliveGmmOne/liveGmmOnestream_20150924/playlist.m3u8&name=ONE_HD&image=ch1hd.png', 'ch1hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('ONE Alternative', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/chonehd&name=ONE_HD&image=ch1hd.png', 'ch1hd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('PPTV', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/chpptv1&name=PPTV_HD&image=chpptvhd.png', 'chpptvhd.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('NOW26', 'playThaiLiveTV&url=rtmp://uk99.seesantv.com/as99/chnow261&name=PPTV_HD&image=chnow26hd.jpg', 'chnow26hd.jpg', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('GMM', 'playThaiLiveTV&url=http://edge4-03.thaimediaserver.com/chliveGreen/liveGreenstream_20150924/playlist.m3u8&name=GMM&image=gmm.png', 'gmm.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('Keera', 'playThaiLiveTV&url=http://edge7-03.thaimediaserver.com/chliveKeera/liveKeerastream_20150924/playlist.m3u8&name=Keera&image=keera.png', 'keera.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('Nation', 'playThaiLiveTV&url=http://edge7-04.thaimediaserver.com/chliveNationNews/liveNationstream_20150924/playlist.m3u8&name=Nation&image=nation.png', 'nation.png', 'DefaultMovies.png', isFolder=False)
        self.addDirectoryItem('Thairath', 'playThaiLiveTV&url=http://edge4-05.thaimediaserver.com/chliveThaiRath/liveThaiRathstream_20150924/playlist.m3u8&name=Nation&image=thairath.png', 'thairath.png', 'DefaultMovies.png', isFolder=False)
        self.endDirectory()
        views.setView('movies', {'skin.confluence': 50})

    def thaiShows(self):
        self.addDirectoryItem('ละครไทย (ออนแอร์) / Thai Dramas (on air)', 'listShows&catid=18', '', 'DefaultMovies.png')
        self.addDirectoryItem('ละครไทย (อวสาน) / Thai Dramas (ended)', 'listShows&catid=27', '', 'DefaultMovies.png')
        self.addDirectoryItem('ซีรี่ย์เกาหลี / Korean Series', 'listShows&catid=17', '', 'DefaultMovies.png')
        self.addDirectoryItem('หนังจีนชุด / Chinese Series', 'listShows&catid=37', '', 'DefaultMovies.png')
        self.addDirectoryItem('รายการอาหาร / Cooking Shows', 'listShows&catid=15', '', 'DefaultMovies.png')
        self.addDirectoryItem('วาไรตี้โชว์ / Variety Shows', 'listShows&catid=8', '', 'DefaultMovies.png')
        self.addDirectoryItem('เรียลลิตี้โชว์ / Reality & Singing Contest', 'listShows&catid=84', '', 'DefaultMovies.png')
        self.addDirectoryItem('ข่าว / Thai News', 'listShows&catid=4', '', 'DefaultMovies.png')
        self.addDirectoryItem('ทอล์กโชว์ / Talk Shows', 'listShows&catid=3', '', 'DefaultMovies.png')
        self.addDirectoryItem('ภาพยนตร์ไทย / Thai Movies', 'listShows&catid=92', '', 'DefaultMovies.png')
        self.addDirectoryItem('ภาพยนตร์ฝรั่งใหม่ / US Movies (Thai dubbed)', 'listShows&catid=98', '', 'DefaultMovies.png')
        self.addDirectoryItem('ซีรี่ย์ฝรั่ง / US Series (Thai dubbed)', 'listShows&catid=38', '', 'DefaultMovies.png')
        self.addDirectoryItem('ภาพยนตร์แอนนิเมชั่น / Animation', 'listShows&catid=93', '', 'DefaultMovies.png')
        self.endDirectory()
        views.setView('movies', {'skin.confluence': 50})

    def thaiShows2(self):
        self.addDirectoryItem('Thai Drama (on air)', 'listShows2&catid=8&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (2015)', 'listShows2&catid=287&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (2014)', 'listShows2&catid=70&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (2013)', 'listShows2&catid=49&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (2012)', 'listShows2&catid=47&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (2011)', 'listShows2&catid=46&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (2010)', 'listShows2&catid=45&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (2009)', 'listShows2&catid=44&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (2008)', 'listShows2&catid=43&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
        self.addDirectoryItem('Thai Drama (classic)', 'listShows2&catid=42&page=1&limit=64&channel=0', '', 'DefaultMovies.png')
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
        views.setView('movies', {'skin.confluence': 50})

    def movies(self):
        self.addDirectoryItem(30021, 'movieGenres', 'movieGenres.jpg', 'DefaultMovies.png')
        #self.addDirectoryItem(30022, 'movieYears', 'movieYears.jpg', 'DefaultMovies.png')
        #self.addDirectoryItem(30023, 'moviePersons', 'movies.jpg', 'DefaultMovies.png')
        #self.addDirectoryItem(30024, 'movieCertificates', 'movieCertificates.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30025, 'movies&url=featured', 'movies.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(30026, 'movies&url=trending', 'moviesTrending.jpg', 'DefaultRecentlyAddedMovies.png')
        #self.addDirectoryItem(30027, 'movies&url=popular', 'moviesPopular.jpg', 'DefaultMovies.png')
        #self.addDirectoryItem(30028, 'movies&url=views', 'moviesViews.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30029, 'movies&url=boxoffice', 'moviesBoxoffice.jpg', 'DefaultMovies.png')
        #self.addDirectoryItem(30030, 'movies&url=oscars', 'moviesOscars.jpg', 'DefaultMovies.png')
        #self.addDirectoryItem(30031, 'movies&url=theaters', 'moviesTheaters.jpg', 'DefaultRecentlyAddedMovies.png')
        #self.addDirectoryItem(30032, 'movies&url=added', 'moviesAdded.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(30033, 'movieFavourites', 'movieFavourites.jpg', 'DefaultMovies.png')
        #self.addDirectoryItem(30034, 'moviePerson', 'moviePerson.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30035, 'movieSearch', 'movieSearch.jpg', 'DefaultMovies.png')

        self.endDirectory()
        views.setView('movies', {'skin.confluence': 50})


    def tvshows(self):
        self.addDirectoryItem(30051, 'tvGenres', 'tvGenres.jpg', 'DefaultTVShows.png')
        #self.addDirectoryItem(30052, 'tvYears', 'tvshows.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30053, 'tvNetworks', 'tvshows.jpg', 'DefaultTVShows.png')
        #self.addDirectoryItem(30054, 'tvshows&url=trending', 'tvshowsTrending.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30055, 'tvshows&url=popular', 'tvshowsPopular.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30056, 'tvshows&url=airing', 'tvshows.jpg', 'DefaultTVShows.png')
        #self.addDirectoryItem(30057, 'tvshows&url=active', 'tvshowsActive.jpg', 'DefaultTVShows.png')
        #self.addDirectoryItem(30058, 'tvshows&url=premiere', 'tvshows.jpg', 'DefaultTVShows.png')
        #self.addDirectoryItem(30059, 'tvshows&url=rating', 'tvshowsRating.jpg', 'DefaultTVShows.png')
        #self.addDirectoryItem(30060, 'tvshows&url=views', 'tvshowsViews.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30061, 'calendars', 'calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')
        #self.addDirectoryItem(30062, 'calendar&url=added', 'calendarsAdded.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30063, 'episodeFavourites', 'tvFavourites.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30064, 'tvFavourites', 'tvFavourites.jpg', 'DefaultTVShows.png')
        #self.addDirectoryItem(30065, 'tvPerson', 'tvPerson.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30066, 'tvSearch', 'tvSearch.jpg', 'DefaultTVShows.png')

        self.endDirectory()
        views.setView('movies', {'skin.confluence': 50})


    def DooFree(self):
        if traktMode == True:
            self.addDirectoryItem(30081, 'movies&url=traktcollection', 'moviesTraktcollection.jpg', 'DefaultMovies.png', context=(30191, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(30082, 'movies&url=traktwatchlist', 'moviesTraktwatchlist.jpg', 'DefaultMovies.png', context=(30191, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(30083, 'movies&url=traktfeatured', 'movies.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30084, 'movies&url=traktratings', 'movies.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30085, 'tvshows&url=traktcollection', 'tvshowsTraktcollection.jpg', 'DefaultTVShows.png', context=(30191, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(30086, 'tvshows&url=traktwatchlist', 'tvshowsTraktwatchlist.jpg', 'DefaultTVShows.png', context=(30191, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(30087, 'tvshows&url=traktfeatured', 'tvshows.jpg', 'DefaultTVShows.png')
            self.addDirectoryItem(30088, 'tvshows&url=traktratings', 'tvshows.jpg', 'DefaultTVShows.png')
            self.addDirectoryItem(30089, 'calendar&url=progress', 'calendarsProgress.jpg', 'DefaultRecentlyAddedEpisodes.png')
            self.addDirectoryItem(30090, 'calendar&url=mycalendar', 'calendarsMycalendar.jpg', 'DefaultRecentlyAddedEpisodes.png')

        if imdbMode == True:
            self.addDirectoryItem(30091, 'movies&url=imdbwatchlist', 'moviesImdbwatchlist.jpg', 'DefaultMovies.png', context=(30191, 'moviesToLibrary&url=imdbwatchlist'))
            self.addDirectoryItem(30092, 'tvshows&url=imdbwatchlist', 'tvshowsImdbwatchlist.jpg', 'DefaultTVShows.png', context=(30191, 'tvshowsToLibrary&url=imdbwatchlist'))

        if traktMode == True or imdbMode == True:
            self.addDirectoryItem(30093, 'movieUserlists', 'movieUserlists.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30094, 'tvUserlists', 'tvUserlists.jpg', 'DefaultTVShows.png')

        self.addDirectoryItem(30095, 'movieFavourites', 'movieFavourites.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30096, 'episodeFavourites', 'tvFavourites.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30097, 'tvFavourites', 'tvFavourites.jpg', 'DefaultTVShows.png')

        self.endDirectory()

    def liveTV(self):
        url = 'http://urhd.tv/'

        html = client.request(url)
        html = client.replaceHTMLCodes(html)

        items = re.findall('channels="(\[.+?\])"', html)[0]
        items = json.loads(items)
        items = [(i['display_name'].replace('_', ' ').replace('-', ' '), i['slug']) for i in items if i['alive'] == True]
        print items
        return items

    def tools(self):
        self.addDirectoryItem(30111, 'openSettings&query=0.0', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30112, 'openSettings&query=6.1', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30113, 'openSettings&query=1.0', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30114, 'openSettings&query=8.0', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30115, 'openSettings&query=2.0', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30116, 'openSettings&query=3.0', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30117, 'openSettings&query=4.0', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30118, 'openSettings&query=5.0', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30119, 'clearSources', 'cache.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30120, 'clearCache', 'cache.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30121, 'libtoolNavigator', 'tools.jpg', 'DefaultAddonProgram.png')

        self.endDirectory()


    def library(self):
        self.addDirectoryItem(30131, 'openSettings&query=7.0', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30132, 'updateLibrary&query=tool', 'update.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30133, control.setting('movie_library'), 'movies.jpg', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(30134, control.setting('tv_library'), 'tvshows.jpg', 'DefaultTVShows.png', isAction=False)

        if traktMode == True:
            self.addDirectoryItem(30135, 'moviesToLibrary&url=traktcollection&query=tool', 'moviesTraktcollection.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30136, 'moviesToLibrary&url=traktwatchlist&query=tool', 'moviesTraktwatchlist.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30137, 'tvshowsToLibrary&url=traktcollection&query=tool', 'tvshowsTraktcollection.jpg', 'DefaultTVShows.png')
            self.addDirectoryItem(30138, 'tvshowsToLibrary&url=traktwatchlist&query=tool', 'tvshowsTraktwatchlist.jpg', 'DefaultTVShows.png')

        if imdbMode == True:
            self.addDirectoryItem(30139, 'moviesToLibrary&url=imdbwatchlist&query=tool', 'moviesImdbwatchlist.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30140, 'tvshowsToLibrary&url=imdbwatchlist&query=tool', 'tvshowsImdbwatchlist.jpg', 'DefaultTVShows.png')

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(30151, 'movieSearch', 'movieSearch.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30152, 'tvSearch', 'tvSearch.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30153, 'moviePerson', 'moviePerson.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30154, 'tvPerson', 'tvPerson.jpg', 'DefaultTVShows.png')

        self.endDirectory()


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


