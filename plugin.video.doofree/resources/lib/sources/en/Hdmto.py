# -*- coding: UTF-8 -*-

import re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 31
		self.language = ['en']
		self.domains = ['hdm.to']
		self.base_link = 'https://hdm.to'
		self.search_link = '/search/%s+%s'


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			t = cleantitle.geturl(title).replace('-', '+').replace('++', '+')
			self.title = t
			url = self.base_link + self.search_link % (t, year)
			print url
			r = client.request(url)
			u = client.parseDOM(r, "div", attrs={"class": "col-md-2 col-sm-2 mrgb"})
			for i in u:
				link = re.compile('<a href="(.+?)"').findall(i)
				for url in link:
					if not cleantitle.get(title) in cleantitle.get(url):
						continue
					return url
		except:
			source_utils.scraper_error('HDMTO')
			return


	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			hostDict = hostDict + hostprDict

			if url is None:
				return sources

			t = client.request(url)

			r = re.compile('<iframe.+?src="(.+?)"').findall(t)
			if r[0]:
				headers = {
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
					'Accept': '*/*',
					'Accept-Encoding': 'identity;q=1, *;q=0',
					'Accept-Language': 'en-US,en;q=0.5',
					'Connection': 'keep-alive',
					'Pragma': 'no-cache',
					'Cache-Control': 'no-cache',
					'DNT': '1'
				}
				response = client.request(r[0], headers=headers)
				vid = r[0].split('//1o.to/')[1]
				url = 'https://1o.to/%s' % (vid)
				sources.append({'source': 'Direct', 'quality': '720p', 'language': 'en', 'url': url + '|Referer=' + r[0], 'direct': True, 'debridonly': False})
				return sources
		except:
			return sources


	def resolve(self, url):
		return url