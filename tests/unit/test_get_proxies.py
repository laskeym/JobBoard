import pytest

import requests
from bs4 import BeautifulSoup

url = 'https://free-proxy-list.net'

def test_get_proxies():
  proxiesPage = requests.get(url)

  if proxiesPage.ok:
    proxies = set()
    pageParser = BeautifulSoup(proxiesPage.content, 'lxml')

    proxyTable = pageParser.find('tbody')
    proxyAddressRows = proxyTable.findChildren('tr')

    for proxyAddressRow in proxyAddressRows:
      proxyColumns = list(proxyAddressRow.children)

      # proxyColumns[6] is the HTTPS column
      if proxyColumns[6].text == 'yes':
        # proxyColumns[0] is the IP Address
        proxies.add(proxyColumns[0].text)
    
    assert len(proxies) > 0
  else:
    return '{} returned with a status code of {}'.format(url, proxiesPage.status_code)