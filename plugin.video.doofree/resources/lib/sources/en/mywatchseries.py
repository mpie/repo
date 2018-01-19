# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['dwatchseries.to']
        self.base_link = 'http://dwatchseries.to'
        self.search_link = '/search/%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query(tvshowtitle)))
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            headers = {'User_Agent': User_Agent, 'referer': self.base_link}
            result = client.request(url.lower().replace('+','%20'), headers=headers)

            link = result.split('Search results')[1:]
            links = re.findall(r'<a href="([^"]+)" title=".*?" target="_blank"><strong>([^<>]*)</strong></a>', str(link), re.I | re.DOTALL)

            for media_url, media_title in links:
                if not cleantitle.get(url.rsplit('/', 1)[-1]).lower().replace('+','') == cleantitle.get(media_title).lower():
                    continue

                headers = {'User_Agent': User_Agent}
                link = client.request(media_url.lower().replace('+','%20'), headers=headers, timeout=10)
                links = link.split('<li id="episode')[1:]
                for p in links:
                    media_url = re.compile('href="([^"]+)"').findall(p)[0]
                    sep = 's%s_e%s' % (season, episode)
                    if sep in media_url.lower():
                        return media_url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User_Agent': User_Agent}
            result = client.request(url.lower().replace('+','%20'), headers=headers, timeout=10)

            rsources = re.findall(r'cale\.html\?r=(.*?)"', str(result), re.I | re.DOTALL)

            uniques = []
            count = 0
            for hosts in rsources:
                final_url = hosts.decode('base64')
                if final_url not in uniques:
                    uniques.append(final_url)

                    host = final_url.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].lower()
                    if not self.filter_host(host):
                        continue
                    host = host.split('.')[0].title()
                    count += 1
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': final_url, 'direct': False, 'debridonly': False})


            return sources
        except:
            return sources

    def resolve(self, url):
        return url

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
