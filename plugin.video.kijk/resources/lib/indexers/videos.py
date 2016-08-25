# -*- coding: utf-8 -*-

from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import views

import sys,os,re,urllib,urlparse,json


class Videos:
    def __init__(self):
        self.list = []
        self.base_link = 'http://upload.kijk.nl'
        self.entitlement_link = '/ajax/entitlement/%s'
        self.embed_link = 'http://embed.kijk.nl/api/roll/%s'
        self.ref_link = 'http://embed.kijk.nl/video/%s'
        self.search_link = 'http://upload.kijk.nl/ajax/kanalen/zoeken/undefined/%s'

    def create_list(self, videos):
        for video in videos:
            action = 'list_video&name=%s&image=%s' % (video[2], video[1])
            self.list.append({'name': video[2], 'url': video[0], 'image': video[1], 'action': action})
        self.add_items(self.list)

    def overview(self, name):
        r = client.request(self.base_link)
        container = re.compile(name + '\<\/h2\>(.+?)\<h2').findall(r)[0]
        videos = re.compile('a href="(.+?)".+?noscript\>.+?src="(.+?)".+?alt="(.+?)".+?\/').findall(container)
        self.create_list(videos)

    def category(self, uri):
        url = urlparse.urljoin(self.base_link, uri)
        r = client.request(url)
        videos = re.compile('a href="(.+?)".+?class="image.+?noscript\>.+?src="(.+?)".+?alt="(.+?)".+?\<a').findall(r)
        self.create_list(videos)

    def list_video(self, name, image, uri):
        vid_hash = re.compile('videos\/(.+)\/').findall(uri)[0]
        e_url = self.entitlement_link % (vid_hash)
        url = urlparse.urljoin(self.base_link, e_url)

        r = client.request(url)
        data = json.loads(r)
        key = data['entitlement']['playerInfo']['hostingkey']

        embed_url = urlparse.urljoin(self.embed_link, key)

        headers = {
            'cache-control': 'no-cache, must-revalidate',
            'Referer': self.ref_link % (vid_hash)
        }
        video_data = client.request(embed_url, headers=headers)
        data = json.loads(video_data)

        for vid in data['streams']:
            action = 'play&name=%s&image=%s' % (name, image)
            self.list.append({'name': vid['name'], 'url': vid['url'], 'image': image, 'action': action})

        self.add_items(self.list)

    def play(self, name, image, uri):
        try:
            from resources.lib.modules.player import player
            item = control.item(label=name, iconImage=image, thumbnailImage=image)
            player().play(uri, item)
        except:
            pass

    def search(self):
        try:
            control.idle()

            k = control.keyboard('', 'Zoeken') ; k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''): return

            url = self.search_link % (urllib.quote_plus(q))
            url = '%s?action=search_results&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            control.execute('Container.Update(%s)' % url)
        except:
            return

    def search_results(self, uri):
        r = client.request(uri)
        r = client.parseDOM(r, 'li')

        r = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'img', ret='src')[0], client.parseDOM(i, 'div', attrs={'class': 'meta'})[0]) for i in r]

        for uri, image, name in r:
            action = 'list_video&name=%s&image=%s' % (name, image)
            self.list.append(
                {
                    'name': name,
                    'url': uri,
                    'image': image,
                    'action': action
                }
            )

        self.add_items(self.list)

    def add_items(self, items, queue=False):
        if items is None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http://'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                cm = []

                if queue == True:
                    cm.append(('Queue item', 'RunPlugin(%s?action=queueItem)' % sysaddon))

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.directory(syshandle, cacheToDisc=True)
        views.setView('videos', {'skin.confluence': 500})
