# -*- coding: utf-8 -*-

import json
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['watchepisodes.com', 'watchepisodes.unblocked.pl']
		self.base_link = 'http://www.watchepisodes4.com/'
		self.search_link = 'search/ajax_search?q=%s'

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if url is None:
				return

			url = urlparse.parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
			url = urllib.urlencode(url)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			if url is None:
				return sources

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle']

			hdlr = 's%02de%02d' % (int(data['season']), int(data['episode']))

			query = urllib.quote_plus(cleantitle.getsearch(title))

			surl = urlparse.urljoin(self.base_link, self.search_link % query)

			r = client.request(surl, XHR=True)
			r = json.loads(r)
			r = r['series']

			for i in r:
				tit = i['value']

				if cleantitle.get(title) != cleantitle.get(tit):
					continue
				slink = i['seo']
				slink = urlparse.urljoin(self.base_link, slink)

				r = client.request(slink)

				if not data['imdb'] in r:
					continue

				data = client.parseDOM(r, 'div', {'class': 'el-item\s*'})

				epis = [client.parseDOM(i, 'a', ret='href')[0] for i in data if i]
				epis = [i for i in epis if hdlr in i.lower()][0]

				r = client.request(epis)
				links = client.parseDOM(r, 'a', ret='data-actuallink')

				for url in links:
					try:
						valid, host = source_utils.is_host_valid(url, hostDict)
						if not valid:
							continue

						if host in ['mixdrop.co', 'upstream.to']:
							sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
					except:
						return sources

			return sources
		except:
			return sources

	def resolve(self, url):
		return url
