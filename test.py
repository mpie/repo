import requests, json
from bs4 import BeautifulSoup

headers_Get = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

result = {}


def google(currency):
    s = requests.Session()
    currency = '+'.join(currency.split())
    url = 'http://www.xe.com/currencyconverter/convert/?From=' + str(currency) + '&To=EUR'
    r = s.get(url, headers=headers_Get)
    print r.text

    soup = BeautifulSoup(r.text, "html.parser")
    for searchWrapper in soup.find_all('span', {'class':'converterresult-toAmount'}):
        print searchWrapper
        # text = searchWrapper.find('strong').text.strip()
        # print text
        # data = {'val': str(text)}
        # result[str(currency) + '_EUR'] = data

google('GBP')
google('CHF')

with open('currencies.json', 'w') as outfile:
    json.dump(result, outfile)
