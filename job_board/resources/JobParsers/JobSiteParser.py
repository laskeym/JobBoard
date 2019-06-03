import requests
from bs4 import BeautifulSoup

from job_board.resources.JobListing import JobListing


class JobSiteParser:
  def __init__(self):
    self.currentPage = None
    self.pageParser = None

  def getPage(self, pageURL, params=None):
    response = requests.get(pageURL, params=params)

    if response.ok:
      return response
    else:
      return None

  def setPage(self, page):
    self.currentPage = page

  def setParser(self, parser='lxml'):
    self.pageParser = BeautifulSoup(self.currentPage.content, parser)

  def getJobListings(self):
    pass

  def getJobListingInfo(self, pageURL):
    jobListingPage = self.getPage(pageURL)
    self.setPage(jobListingPage)
    self.setParser()

    self.jobListing = JobListing()