import requests
from bs4 import BeautifulSoup

URL = 'https://free-proxy-list.net'
proxies = set()

def getProxies():
  proxyPage = getFreeProxyPage()

  if proxyPage:
    proxyTableRows = getProxyTableRows(proxyPage)
    for proxyTableRow in proxyTableRows:
      proxyRowColumns = list(proxyTableRow.children)
      if validateProxyTableRow(proxyRowColumns):
        # proxyRowColumns[0] is the IP Address column
        proxies.add(proxyRowColumns[0].text)

  return proxies

def getFreeProxyPage():
  page = requests.get(URL)

  if page.ok:
    return page

def getProxyTableRows(proxyPage):
  pageParser = BeautifulSoup(proxyPage.content, 'lxml')

  proxyTableBody = pageParser.find('tbody')
  proxyAddressRows = proxyTableBody.findChildren('tr')

  return proxyAddressRows

def validateProxyTableRow(proxyTableRow):
  """
  If the HTTPS column in the row is marked as 'yes', then return the IP Address
  """
  if proxyTableRow[6].text == 'yes':
    return True
