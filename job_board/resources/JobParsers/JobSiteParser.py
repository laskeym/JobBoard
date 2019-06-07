import requests
from bs4 import BeautifulSoup

from job_board.resources.JobListing import JobListing
from job_board.resources.Error import ResponseNotOKError


class JobSiteParser:
  def __init__(self):
    self.currentPage = None
    self.pageParser = None

  def getPage(self, pageURL, params=None):
    response = requests.get(pageURL, params=params)

    if response.ok:
      return response
    else:
      raise ResponseNotOKError(pageURL, response.status_code)

  def setPage(self, page):
    self.currentPage = page

  def setParser(self, parser='lxml'):
    self.pageParser = BeautifulSoup(self.currentPage.content, parser)

  def parseJobListings(self, jobListings):
    pass

  def createJobListing(self, jobListing):
    pass