# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import urllib, urllib2, re, gzip, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, sys, os

from resources.lib.modules import control
from resources.lib.modules import client

addonFanart = control.addonFanart()
syshandle = int(sys.argv[1])
sysaddon = sys.argv[0]

urlopen = urllib2.urlopen
Request = urllib2.Request


class livetv:
    def __init__(self):
        self.USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        self.headers = {'User-Agent': self.USER_AGENT, 'Accept': '*/*','Connection': 'keep-alive'}
        socket.setdefaulttimeout(10)

        self.base_link = 'http://iptvsatlinks.blogspot.com/search?max-results=40'

    def addDir(self, name, url, action, icon, Folder=True):
        if url.startswith('plugin'):
            u = url
        else:
            u = (sysaddon +
                 "?url=" + urllib.quote_plus(url) +
                 "&name=" + urllib.quote_plus(name) +
                 "&action=" + action)

        item = control.item(label=name)

        item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

        ok = control.addItem(handle=syshandle, url=u, listitem=item, isFolder=Folder)
        return ok

    def index(self):
        txtfilter = self.getFilter()
        if not txtfilter:
            txtfilter = "none"
        self.addDir('[B]Current filter:[/B] ' + txtfilter, '', 'openSettings', '', Folder=False)
        html = client.request(self.base_link)
        blogpage = re.compile("content='([^']+)' itemprop='image_url'.*?href='([^']+)'>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(html)
        for img, url, name in blogpage:
            self.addDir(name, url, 'listStreams', img)
        try:
            nextp = re.compile("'blog-pager-older-link' href='([^']+)'", re.DOTALL | re.IGNORECASE).findall(html)[0]
            nextp = nextp.replace('&amp;', '&')
            self.addDir(control.lang(32053).encode('utf-8'), nextp, 'liveTV', control.addonNext())
        except:
            pass
        xbmcplugin.endOfDirectory(syshandle)

    def listStreams(self, url):
        html = client.request(url)
        blogpage = re.compile('<div class="code">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(html)[0]
        if '#EXTINF' in blogpage:
            blogpage = blogpage.replace('<br />', '\n').replace('&nbsp;', '').replace('&amp;', '&')
            self.parsem3u(blogpage, False)
        else:
            txtfilter = self.getFilter()
            if txtfilter:
                self.addDir('Search all links for: ' + txtfilter, url, 'searchLiveTVLinks', '')
            iptvlinks = re.compile("(h[^<]+)", re.DOTALL | re.IGNORECASE).findall(blogpage)
            i = 1
            for link in iptvlinks:
                link = link.replace('&amp;', '&')
                name = 'Link ' + str(i) + ': ' + link
                self.addDir(name, link, 'getLiveTVurl', '')
                i += 1
        xbmcplugin.endOfDirectory(syshandle)

    def getLiveTVurl(self, url):
        try:
            m3u = self.getHtml(url)
            self.parsem3u(m3u, False)
        except:
            self.addDir('Nothing found', '', '', '', Folder=False)
        xbmcplugin.endOfDirectory(syshandle)

    def getFilter(self):
        filterset = int(control.setting('filterset')) + 1
        txtfilter = control.setting('txtfilter' + str(filterset))
        return txtfilter

    def parsem3u(self, html, sitechk=True):
        match = re.compile('#.+,(.+?)\n(.+?)\n').findall(html)
        txtfilter = self.getFilter()
        txtfilter = txtfilter.split(',') if txtfilter else []
        txtfilter = [f.lower().strip() for f in txtfilter]
        i = 0
        count = 0
        self.addDir('[B]Try a different stream if the one you want is down![/B]', '', '', '', Folder=False)
        for name, url in match:
            status = ""
            url = url.replace('\r', '')
            if not txtfilter or any(f in name.lower() for f in txtfilter):
                if sitechk:
                    if i < 3:
                        try:
                            siteup = urllib.urlopen(url).getcode()
                            status = " [COLOR red]offline[/COLOR]" if siteup != 200 else " [COLOR green]online[/COLOR]"
                        except:
                            status = " [COLOR red]offline[/COLOR]"
                        i += 1
                self.addPlayLink(name + status, url, 'playLiveTV', '')
                count += 1
        return count

    def searchLinks(self, url):
        txtfilter = self.getFilter()
        count = 0
        dp = xbmcgui.DialogProgress()
        dp.create("Searching LiveTV lists", "Searching for:", txtfilter)
        html = client.request(url)
        blogpage = re.compile('<div class="code">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(html)[0]
        iptvlinks = re.compile("(h[^<]+)", re.DOTALL | re.IGNORECASE).findall(blogpage)
        addcount = 100 / len(iptvlinks)
        for link in iptvlinks:
            dp.update(int(count))
            link = link.replace('&amp;', '&')
            try:
                listup = urllib.urlopen(link).getcode()
                if listup == 200:
                    m3u = self.getHtml(link)
                    links = self.parsem3u(m3u, False)
                    count = count + addcount
                    if links > 1:
                        self.addDir('---------------------', '', 'listStreams', '', Folder=False)
            except:
                count = count + addcount
                pass
        dp.close()
        xbmcplugin.endOfDirectory(syshandle)

    def getHtml(self, url, referer=None, hdr=None, data=None):
        if not hdr:
            req = Request(url, data, self.headers)
        else:
            req = Request(url, data, hdr)
        if referer:
            req.add_header('Referer', referer)
        if data:
            req.add_header('Content-Length', len(data))
        response = urlopen(req, timeout=20)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            f.close()
        else:
            data = response.read()
        response.close()
        return data

    def addPlayLink(self, name, url, action, iconimage):
        u = (sysaddon +
             "?url=" + urllib.quote_plus(url) +
             "&action=" + action +
             "&name=" + urllib.quote_plus(name))

        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setArt({'thumb': iconimage, 'icon': iconimage})
        liz.setInfo(type="Video", infoLabels={"Title": name})
        video_streaminfo = {'codec': 'h264'}
        liz.addStreamInfo('video', video_streaminfo)
        ok = xbmcplugin.addDirectoryItem(handle=syshandle, url=u, listitem=liz, isFolder=False)
        return ok

    def openSettings(self):
        control.openSettings('7.1')
        xbmc.executebuiltin('Container.Refresh')



