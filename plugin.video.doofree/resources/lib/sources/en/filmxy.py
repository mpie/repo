# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['filmxy.me']
        self.base_link = 'http://www.filmxy.me'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def filter_host(self, host):
        if host not in ['example.com', 'allvid.ch', 'anime-portal.org', 'anyfiles.pl',
                        'www.apnasave.club', 'castamp.com', 'clicknupload.com', 'clicknupload.me',
                        'clicknupload.link', 'cloud.mail.ru', 'cloudy.ec', 'cloudy.eu', 'cloudy.sx',
                        'cloudy.ch', 'cloudy.com', 'daclips.in', 'daclips.com', 'dailymotion.com',
                        'ecostream.tv', 'exashare.com', 'uame8aij4f.com', 'yahmaib3ai.com',
                        'facebook.com', 'filepup.net', 'fileweed.net', 'flashx.tv', 'googlevideo.com',
                        'googleusercontent.com', 'get.google.com', 'plus.google.com', 'googledrive.com',
                        'drive.google.com', 'docs.google.com', 'gorillavid.in', 'gorillavid.com',
                        'grifthost.com', 'hugefiles.net', 'indavideo.hu', 'kingfiles.net', 'mail.ru',
                        'my.mail.ru', 'm.my.mail.ru', 'videoapi.my.mail.ru', 'api.video.mail.ru',
                        'mersalaayitten.com', 'mersalaayitten.co', 'mersalaayitten.us', 'movdivx.com',
                        'divxme.com', 'movpod.net', 'movpod.in', 'movshare.net', 'wholecloud.net',
                        'vidgg.to', 'mp4stream.com', 'myvi.ru', 'nosvideo.com', 'noslocker.com',
                        'novamov.com', 'auroravid.to', 'ok.ru', 'odnoklassniki.ru', 'openload.io',
                        'openload.co', 'oload.tv', 'playwire.com', 'promptfile.com', 'rapidvideo.com',
                        'raptu.com', 'rutube.ru', 'videos.sapo.pt', 'speedvideo.net', 'streamcloud.eu',
                        'streamin.to', 'stream.moe', 'streamplay.to', 'teramixer.com', 'thevid.net',
                        'thevideo.me', 'toltsd-fel.tk', 'toltsd-fel.xyz', 'trollvid.net', 'trollvid.io',
                        'mp4edge.com', 'tudou.com', 'tune.pk', 'upload.af', 'uploadx.org', 'uploadz.co',
                        'uptobox.com', 'uptostream.com', 'veoh.com', 'videa.hu', 'videoget.me',
                        'videohut.to', 'videoraj.ec', 'videoraj.eu', 'videoraj.sx', 'videoraj.ch',
                        'videoraj.com', 'videoraj.to', 'videoraj.co', 'bitvid.sx', 'videoweed.es',
                        'videoweed.com', 'videowood.tv', 'byzoo.org', 'playpanda.net', 'videozoo.me',
                        'videowing.me', 'easyvideo.me', 'play44.net', 'playbb.me', 'video44.net',
                        'vidlox.tv', 'vidmad.net', 'tamildrive.com', 'vid.me', 'vidup.me', 'vimeo.com',
                        'vivo.sx', 'vk.com', 'vshare.eu', 'watchers.to', 'watchonline.to',
                        'everplay.watchpass.net', 'weshare.me', 'xvidstage.com', 'yourupload.com',
                        'yucache.net', 'youtube.com', 'youtu.be', 'youtube-nocookie.com',
                        'youwatch.org', 'chouhaa.info', 'aliez.me', 'ani-stream.com', 'bestream.tv',
                        'blazefile.co', 'divxstage.eu', 'divxstage.net', 'divxstage.to', 'cloudtime.to',
                        'downace.com', 'entervideo.net', 'estream.to', 'fastplay.sx', 'fastplay.cc',
                        'goodvideohost.com', 'jetload.tv', 'letwatch.us', 'letwatch.to', 'vidshare.us',
                        'megamp4.net', 'mp4engine.com', 'mp4upload.com', 'myvidstream.net',
                        'nowvideo.eu', 'nowvideo.ch', 'nowvideo.sx', 'nowvideo.co', 'nowvideo.li',
                        'nowvideo.fo', 'nowvideo.at', 'nowvideo.ec', 'playedto.me', 'www.playhd.video',
                        'www.playhd.fo', 'putload.tv', 'shitmovie.com', 'rapidvideo.ws',
                        'speedplay.xyz', 'speedplay.us', 'speedplay1.site', 'speedplay.pw',
                        'speedplay1.pw', 'speedplay3.pw', 'speedplayy.site', 'speedvid.net',
                        'spruto.tv', 'stagevu.com', 'streame.net', 'thevideos.tv', 'tusfiles.net',
                        'userscloud.com', 'usersfiles.com', 'vidabc.com', 'vidcrazy.net',
                        'uploadcrazy.net', 'thevideobee.to', 'videocloud.co', 'vidfile.net',
                        'vidhos.com', 'vidto.me', 'vidtodo.com', 'vidup.org', 'vidzi.tv', 'vodlock.co',
                        'vshare.io', 'watchvideo.us', 'watchvideo2.us', 'watchvideo3.us',
                        'watchvideo4.us', 'watchvideo5.us', 'watchvideo6.us', 'watchvideo7.us',
                        'watchvideo8.us', 'watchvideo9.us', 'watchvideo10.us', 'watchvideo11.us',
                        'watchvideo12.us', 'zstream.to']:
            return False
        return True

    def get_rd_domains(self):
        return ['1fichier.com', 'alterupload.com', 'cjoint.net', 'desfichiers.com', 'dfichiers.com', 'megadl.fr',
                'mesfichiers.org', 'piecejointe.net', 'pjointe.com', 'tenvoi.com', 'dl4free.com', '24uploading.com',
                '2shared.com', '4shared.com', 'alfafile.net', 'uploadable.ch', 'bigfile.to', 'bitporno.com',
                'catshare.net', 'cbs.com', 'clicknupload.me', 'clicknupload.com', 'clicknupload.link',
                'clicknupload.org', 'cloudtime.to', 'divxstage.e', 'divxstage.to', 'dailymotion.com',
                'datafile.com', 'datafilehost.com', 'datei.to', 'datoporn.co', 'depfile.com', 'i-filez.com',
                'dipfile.com', 'depfile.us', 'dl.free.fr', 'easybytez.com', 'exashare.com', 'bojem3a.info',
                'ajihezo.info', 'ohbuegh3ev.com', 'extmatrix.com', 'faststore.org', 'filefactory.com',
                'fileflyer.com', 'fileover.net', 'filerio.com', 'filerio.in', 'filesabc.com', 'filesflash.com',
                'filesflash.net', 'filesmonster.com', 'flashx.tv', 'gigapeta.com', 'gigasize.com', 'docs.google.com',
                'drive.google.com', 'gboxes.com', 'gulfup.com', 'hitfile.net', 'hulkshare.com', 'icerbox.com',
                'inclouddrive.com', 'keep2share.cc', 'k2s.cc', 'keep2s.cc', 'k2share.cc', 'load.to', 'mediafire.com',
                'mega.co.nz', 'mega.nz', 'mightyupload.com', 'movshare.net', 'wholecloud.net', 'nitroflare.com',
                'novamov.com', 'auroravid.to', 'nowdownload.e', 'nowdownload.ch', 'nowdownload.sx', 'nowdownload.ag',
                'nowdownload.at', 'nowdownload.ec', 'nowdownload.li', 'nowdownload.to', 'nowvideo.e', 'nowvideo.ch',
                'nowvideo.sx', 'nowvideo.ag', 'nowvideo.at', 'nowvideo.li', 'oboom.com', 'openload.co', 'openload.io',
                'oload.tv', 'oload.info', 'oload.stream', 'ozofiles.com', 'sky.fm', 'radiotunes.com', 'di.fm',
                'classicalradio.com', 'jazzradio.com', 'rapidgator.net', 'rg.to', 'rapidvideo.com', 'rarefile.net',
                'real-debrid.com', 'redbunker.net', 'redtube.com', 'canalplus.fr', 'd8.tv', 'c8.fr', 'mycanal.fr',
                'rockfile.e', 'rutube.r', 'salefiles.com', 'scribd.com', 'sendspace.com', 'share-online.biz',
                'solidfiles.com', 'soundcloud.com', 'streamango.com', 'streamcherry.com', 'streamin.to',
                'thevideo.me', 'thevideo.io', 'tvad.me', 'turbobit.net', 'tusfiles.net', 'ulozto.net', 'uloz.to',
                'ulozto.sk', 'unibytes.com', 'upload.af', 'upload.mn', 'uploadc.com', 'uploadc.ch', 'uploaded.net',
                'uploaded.to', 'ul.to', 'uploading.com', 'uploading.site', 'uploadrocket.net', 'uploadx.org',
                'uploadx.link', 'upstore.net', 'uptobox.com', 'uptostream.com', 'userporn.com', 'userscloud.com',
                'veevr.com', 'videoweed.es', 'bitvid.sx', 'vidlox.tv', 'vidoza.net', 'vimeo.com', 'vk.com',
                'wipfiles.net', 'worldbytez.com', 'youporn.com', 'youtube.com', 'youwatch.org', 'chouhaa.info',
                'sikafika.info', 'ay8ou8ohth.com', 'voodaith7e.com', 'yunfile.com', 'filemarkets.com', '5xpan.com',
                'dix3.com', 'dfpan.com', 'zippyshare.com']

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year']

            search_id = cleantitle.getsearch(title.lower())
            query = urlparse.urljoin(self.base_link, self.search_link % (search_id.replace(' ','+')))
            result = client.request(query)

            match = re.compile('class="post-thumbnail".+?href="(.+?)".+?class="post-title".+?<h2>(.+?)</h2>', re.DOTALL).findall(result)
            for mov_url, mov_tit in match:
                chk_tit = mov_tit.split('(')[0].strip()
                if cleantitle.getsearch(title).lower() == cleantitle.getsearch(chk_tit).lower():
                    if year in mov_tit:
                        if '/links/' in mov_url:
                            result = client.request(mov_url)
                            block720 = re.compile('class="links_720p"(.+?)</ul>', re.DOTALL).findall(result)
                            Regex = re.compile('href="(.+?)"', re.DOTALL).findall(str(block720))

                            for link in Regex:
                                host = link.split('//')[1].replace('www.', '')
                                host = host.split('/')[0].lower()
                                if not self.filter_host(host):
                                    continue
                                rd_domains = self.get_rd_domains()
                                if host in rd_domains:
                                    sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': True})
                                else:
                                    sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})

                            block1080 = re.compile('class="links_1080p"(.+?)</ul>', re.DOTALL).findall(result)
                            Regex2 = re.compile('href="(.+?)"', re.DOTALL).findall(str(block1080))
                            for link in Regex2:
                                host = link.split('//')[1].replace('www.', '')
                                host = host.split('/')[0].lower()
                                if not self.filter_host(host):
                                    continue
                                rd_domains = self.get_rd_domains()
                                if host in rd_domains:
                                    sources.append({'source': host, 'quality': '1080p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': True})
                                else:
                                    sources.append({'source': host, 'quality': '1080p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url



