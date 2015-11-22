# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2015 Mpie
'''


import urlparse,sys
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))


try:
    action = params['action']
except:
    action = None
try:
    name = params['name']
except:
    name = None
try:
    title = params['title']
except:
    title = None
try:
    channel = params['channel']
except:
    channel = None
try:
    catid = params['catid']
except:
    catid = None
try:
    showid = params['showid']
except:
    showid = None
try:
    showtype = params['showtype']
except:
    showtype = None
try:
    page = params['page']
except:
    page = 0



try:
    year = params['year']
except:
    year = None
try:
    imdb = params['imdb']
except:
    imdb = '0'
try:
    tmdb = params['tmdb']
except:
    tmdb = '0'
try:
    tvdb = params['tvdb']
except:
    tvdb = '0'
try:
    tvrage = params['tvrage']
except:
    tvrage = '0'
try:
    season = params['season']
except:
    season = None
try:
    episode = params['episode']
except:
    episode = None
try:
    tvshowtitle = params['tvshowtitle']
except:
    tvshowtitle = None
try:
    tvshowtitle = params['show']
except:
    pass
try:
    alter = params['alter']
except:
    alter = '0'
try:
    alter = params['genre']
except:
    pass
try:
    date = params['date']
except:
    date = None
try:
    url = params['url']
except:
    url = None
try:
    image = params['image']
except:
    image = None
try:
    meta = params['meta']
except:
    meta = None
try:
    query = params['query']
except:
    query = None
try:
    source = params['source']
except:
    source = None
try:
    content = params['content']
except:
    content = None
try:
    provider = params['provider']
except:
    provider = None

print 'action:' + str(action)

if action == None:
    from resources.lib.indexers import navigator
    navigator.navigator().root()

# Start thai stuff
elif action == 'thaiLiveTV':
    from resources.lib.indexers import navigator
    navigator.navigator().thaiLiveTV()

elif action == 'playThaiLiveTV':
    from resources.lib.sources import sources
    sources().playLiveStream(name, url, image)

elif action == 'thaiShows':
    from resources.lib.indexers import navigator
    navigator.navigator().thaiShows()

elif action == 'listShows':
    from resources.lib.indexers import thai
    thai.thai().listShows(catid, page)

elif action == 'listEpisodes':
    from resources.lib.indexers import thai
    thai.thai().listEpisodes(catid, showid, page, image)

elif action == 'sourcePage':
    from resources.lib.indexers import thai
    thai.thai().sourcePage(url, name, image)
# End thai stuff

# Start movie stuff










elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'myNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().genesis()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'libtoolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieFavourites':
    from resources.lib.indexers import movies
    movies.movies().favourites()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search(query)

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person(query)

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons()

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'channels':
    from resources.lib.indexers import channels
    channels.channels().get()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvFavourites':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().favourites()

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search(query)

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person(query)

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvYears':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().years()

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'episodeFavourites':
    from resources.lib.indexers import episodes
    episodes.episodes().favourites()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'refresh':
    from resources.lib.libraries import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.libraries import control
    control.queueItem()

elif action == 'openPlaylist':
    from resources.lib.libraries import control
    control.openPlaylist()

elif action == 'openSettings':
    from resources.lib.libraries import control
    control.openSettings(query)

elif action == 'moviePlaycount':
    from resources.lib.libraries import playcount
    playcount.movies(title, year, imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.libraries import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.libraries import playcount
    playcount.tvshows(name, year, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.libraries import trailer
    trailer.trailer().play(name, url)

elif action == 'clearCache':
    from resources.lib.libraries import cache
    cache.clear()

elif action == 'addFavourite':
    from resources.lib.libraries import favourites
    favourites.addFavourite(meta, content, query)

elif action == 'deleteFavourite':
    from resources.lib.libraries import favourites
    favourites.deleteFavourite(meta, content)

elif action == 'addView':
    from resources.lib.libraries import views
    views.addView(content)

elif action == 'traktManager':
    from resources.lib.libraries import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'movieToLibrary':
    from resources.lib.libraries import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.libraries import libtools
    libtools.libmovies().range(url, query)

elif action == 'tvshowToLibrary':
    from resources.lib.libraries import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tmdb, tvdb, tvrage)

elif action == 'tvshowsToLibrary':
    from resources.lib.libraries import libtools
    libtools.libtvshows().range(url, query)

elif action == 'updateLibrary':
    from resources.lib.libraries import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.libraries import libtools
    libtools.libepisodes().service()

elif action == 'resolve':
    from resources.lib.sources import sources
    from resources.lib.libraries import control
    url = sources().sourcesResolve(url, provider)
    control.addItem(handle=int(sys.argv[1]), url=url, listitem=control.item(name))
    control.directory(int(sys.argv[1]))

elif action == 'play':
    from resources.lib.sources import sources
    sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, url)

elif action == 'sources':
    from resources.lib.sources import sources
    sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)

elif action == 'playItem':
    from resources.lib.sources import sources
    sources().playItem(content, name, imdb, tvdb, url, source, provider)

elif action == 'alterSources':
    from resources.lib.sources import sources
    sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.sources import sources
    sources().clearSources()


