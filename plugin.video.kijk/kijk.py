# -*- coding: utf-8 -*-

import urlparse,sys

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

name = params.get('name')

title = params.get('title')

url = params.get('url')

image = params.get('image')

if action is None:
    from resources.lib.indexers import navigator
    navigator.navigator().root()

elif action == 'overview':
    from resources.lib.indexers import videos
    videos.Videos().overview(name)

elif action == 'category':
    from resources.lib.indexers import videos
    videos.Videos().category(url)

elif action == 'list_video':
    from resources.lib.indexers import videos
    videos.Videos().list_video(name, image, url)

elif action == 'play':
    from resources.lib.indexers import videos
    videos.Videos().play(name, image, url)

elif action == 'search':
    from resources.lib.indexers import videos
    videos.Videos().search()

elif action == 'search_results':
    from resources.lib.indexers import videos
    videos.Videos().search_results(url)
