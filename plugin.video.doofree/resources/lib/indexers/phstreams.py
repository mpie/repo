# -*- coding: utf-8 -*-

import re,sys,urllib

from resources.lib.libraries import cache
from resources.lib.libraries import control
from resources.lib.libraries import views

def getDirectory(url):
    f = control.openFile(url)
    result = f.read()
    f.close()

    result = str(result).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    fanart = '0'
    content = 'movies'
    items = re.compile('<item>(.+?)</item>').findall(result)

    try: sort = re.findall('<sort>(.+?)</sort>', result)[0]
    except: sort = ''
    if sort == 'yes': items = sorted(items)
    totalItems = len(items)

    for item in items:
        try:
            data = {}

            try: name = re.findall('<title>(.+?)</title>', item)[0]
            except: continue

            url = re.findall('<link>(.+?)</link>', item)[0]

            try: image = image2 = re.findall('<thumbnail>(.+?)</thumbnail>', item)[0]
            except: image = image2 = '0'

            try: fanart2 = re.findall('<fanart>(.+?)</fanart>', item)[0]
            except: fanart2 = fanart

            try:
                title = cleantitle(name).encode('utf-8')
                data = {'title': title}

                title, year = re.compile('(.+?)[(](\d{4})[)]').findall(name)[0]
                title = cleantitle(title).encode('utf-8')
                data = {'title': title, 'year': year}
            except:
                pass

            addDirectoryItem(name, url, 'phResolveUrl', image, image2, fanart2, content, data, totalItems=totalItems, isFolder=False)
        except:
            pass

    endDirectory(content, True)

def clearSearch():
    cache.clear('rel_srch')
    control.refresh()

def resolveUrl(name, url, image, fanart, playable, content):
    try:
        if url.startswith('$base64'):
            import base64 ; url = base64.b64decode(re.compile('\$base64\[(.+?)\]$').findall(url)[0])
        label = cleantitle(name)
        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type='Video', infoLabels = {'title': label} )
        control.playlist.clear()
        control.player.play(url, item)
    except:
        pass


def addDirectoryItem(name, url, action, image, image2, fanart, content, data, tvshow='0', totalItems=0, isFolder=True):
    if not str(image).lower().startswith('http'): image = control.addonInfo('icon')

    if not str(image2).lower().startswith('http'): image2 = control.addonInfo('icon')

    if not str(fanart).lower().startswith('http'): fanart = control.addonInfo('fanart')

    if content in ['movies', 'episodes']: playable = 'true'
    else: playable = 'false'

    sysaddon = sys.argv[0]

    if url.startswith('$base64'):
        import base64 ; url = base64.b64decode(re.compile('\$base64\[(.+?)\]$').findall(url)[0])
    u = '%s?name=%s&url=%s&tvdb=&imdb=&source=GVideo&provider=Mpie&content=%s&action=playItem' % (sysaddon, urllib.quote_plus(name), urllib.quote_plus(url), str(content))

    cm = []

    if content == 'movies':
        cm.append((control.lang(30708).encode('utf-8'), 'XBMC.Action(Info)'))
    elif content in ['tvshows', 'seasons']:
        cm.append((control.lang(30709).encode('utf-8'), 'XBMC.Action(Info)'))
    elif content == 'episodes':
        cm.append((control.lang(30710).encode('utf-8'), 'XBMC.Action(Info)'))


    if content == 'movies' and not isFolder == True:
        downloadFile = name
        try: downloadFile = '%s (%s)' % (data['title'], data['year'])
        except: pass
        cm.append((control.lang(30722).encode('utf-8'), 'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)' % (sysaddon, urllib.quote_plus(downloadFile), urllib.quote_plus(url), urllib.quote_plus(image))))

    elif content == 'episodes' and not isFolder == True:
        downloadFile = name
        try: downloadFile = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
        except: pass
        cm.append((control.lang(30722).encode('utf-8'), 'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)' % (sysaddon, urllib.quote_plus(downloadFile), urllib.quote_plus(url), urllib.quote_plus(image))))


    if content == 'movies':
        cm.append((control.lang(30711).encode('utf-8'), 'RunPlugin(%s?action=addView&content=movies)' % sysaddon))
    elif content == 'tvshows':
        cm.append((control.lang(30712).encode('utf-8'), 'RunPlugin(%s?action=addView&content=tvshows)' % sysaddon))
    elif content == 'seasons':
        cm.append((control.lang(30713).encode('utf-8'), 'RunPlugin(%s?action=addView&content=seasons)' % sysaddon))
    elif content == 'episodes':
        cm.append((control.lang(30714).encode('utf-8'), 'RunPlugin(%s?action=addView&content=episodes)' % sysaddon))


    item = control.item(name, iconImage='DefaultFolder.png', thumbnailImage=image)
    try: item.setArt({'poster': image2, 'tvshow.poster': image2, 'season.poster': image2, 'banner': image, 'tvshow.banner': image, 'season.banner': image})
    except: pass
    item.addContextMenuItems(cm, replaceItems=False)
    item.setProperty('Fanart_Image', fanart)
    if playable == 'true': item.setProperty('IsPlayable', 'true')
    item.setInfo(type='Video', infoLabels=data)

    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=totalItems,isFolder=isFolder)


def endCategory():
    if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(500)')
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def endDirectory(content, close):
    if content in ['movies', 'tvshows', 'seasons', 'episodes']:
        control.content(int(sys.argv[1]), content)

    if close == True: control.directory(int(sys.argv[1]), cacheToDisc=True)

    if close == True and content in ['movies', 'tvshows', 'seasons', 'episodes']:
        views.setView(content)


def cleantitle(name):
    name = re.sub('(\.|\_|\(|\[|\s)(Link \d*|link \d*)(\.|\_|\)|\]|$)', '', name)
    name = re.sub('\(\d{4}.+?\d{4}\)$', '', name)
    name = re.sub('\s\[COLOR.+?\].+?\[/COLOR\]|\[/COLOR\]\[COLOR.+?\]\s.+?\[/COLOR\]|\[COLOR.+?\]|\[/COLOR\]', '', name)
    name = re.sub('\s\s+', ' ', name)
    name = name.strip()
    return name


def cleaneptitle(tvshow, name):
    try:
        p = re.compile('(S\d*E\d*)').findall(name)
        p += re.compile('(s\d*e\d*)').findall(name)
        p += re.compile('(Season \d* Episode \d*)').findall(name)
        p += re.compile('(\d*x Episode \d*)').findall(name)
        p += re.compile('(\d*x\d*)').findall(name)
        p = p[0]

        name = name.replace(tvshow, '').replace(p, '')
        name = re.sub('-|:', '', name)
        name = re.sub('\s\s+', ' ', name)
        name = name.strip()

        season = re.compile('(\d*)').findall(p)
        season = [i for i in season if i.isdigit()][0]
        season = '%01d' % int(season)

        episode = re.compile('(\d*)').findall(p)
        episode = [i for i in episode if i.isdigit()][-1]
        episode = '%01d' % int(episode)

        if re.match('[A-Z0-9]', name) == None:
            name = '%s S%02dE%02d' % (tvshow, int(season), int(episode))

        return (name, season, episode)
    except:
        return
