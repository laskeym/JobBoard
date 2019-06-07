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
      # Throw ResponseNotOK exception along with page URL and status code
      return None

  def setPage(self, page):
    self.currentPage = page

  def setParser(self, parser='lxml'):
    self.pageParser = BeautifulSoup(self.currentPage.content, parser)

  def parseJobListings(self):
    pass

  def parseJobListingInfo(self, pageURL):
    jobListingPage = self.getPage(pageURL)

    # This should now be handled by the above exception
    if jobListingPage is not None:
      self.setPage(jobListingPage)
      self.setParser()

      self.jobListing = JobListing()