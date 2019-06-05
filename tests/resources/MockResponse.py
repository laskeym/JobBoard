import os
from urllib.parse import urljoin

mockStackOverflowURL = 'https://www.stackoverflow.com'
mockMonsterURL = 'https://www.monster.com'

def getTestHTMLPage(file_path):
  f = open(file_path)
  html = f.read()
  f.close()

  return html

mockStackOverflowJobListingsFile = os.getcwd() + '/tests/resources/testHTMLPages/StackOverflow/jobListingsPage.html'
mockStackOverflowJobListings = getTestHTMLPage(mockStackOverflowJobListingsFile)

mockStackOverflowJobInfoFile = os.getcwd() + '/tests/resources/testHTMLPages/StackOverflow/jobListingInfoPage.html'
mockStackOverflowJobInfo = getTestHTMLPage(mockStackOverflowJobInfoFile)

mockMonsterJobListingsFile = os.getcwd() + '/tests/resources/testHTMLPages/Monster/jobListingsPage.html'
mockMonsterJobListings = getTestHTMLPage(mockMonsterJobListingsFile)

mockMonsterJobInfoFile = os.getcwd() + '/tests/resources/testHTMLPages/Monster/jobListingInfoPage.html'
mockMonsterJobInfo = getTestHTMLPage(mockMonsterJobInfoFile)

class MockResponse:
  def __init__(self, content, ok=True):
    self.content = content
    self.ok = ok

def mocked_requests_get(*args, **kwargs):
  # StackOverflow
  if args[0] == mockStackOverflowURL:
    return MockResponse(mockStackOverflowJobListings)
  elif args[0] == urljoin(mockStackOverflowURL, 'jobs'):
    return MockResponse(mockStackOverflowJobInfo)  
  # Monster
  elif args[0] == mockMonsterURL:
    return MockResponse(mockMonsterJobListings)
  elif args[0] == urljoin(mockMonsterURL, 'jobs/search'):
    return MockResponse(mockMonsterJobInfo)