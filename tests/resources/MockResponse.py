import os
from urllib.parse import urljoin

mockStackOverflowURL = 'https://www.stackoverflow.com'

def getTestHTMLPage(file_path):
  f = open(file_path)
  html = f.read()
  f.close()

  return html

mockJobListingsPageFile = os.getcwd() + '/tests/resources/testHTMLPages/StackOverflow/jobListingsPage.html'
mockJobListingsPage = getTestHTMLPage(mockJobListingsPageFile)

mockJobListingInfoPageFile = os.getcwd() + '/tests/resources/testHTMLPages/StackOverflow/jobListingInfoPage.html'
mockJobListingInfoPage = getTestHTMLPage(mockJobListingInfoPageFile)

class MockResponse:
  def __init__(self, content, ok):
    self.content = content
    self.ok = ok

def mocked_requests_get(*args, **kwargs):
  if args[0] == mockStackOverflowURL:
    return MockResponse(mockJobListingsPage, True)
  elif args[0] == urljoin(mockStackOverflowURL, 'jobs'):
    return MockResponse(mockJobListingInfoPage, True)  