import random

import requests
from bs4 import BeautifulSoup

from job_board.utilities.getProxies import getProxies
from job_board.resources.JobListing import JobListing


class JobSiteParser:
  def __init__(self):
    self.currentPage = None
    self.pageParser = None
    self.proxies = list(getProxies())

  def getPage(self, pageURL, params=None):
    headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    response = requests.get(pageURL, params=params, headers=headers)

    if response.ok:
      return response
    else:
      return None

  def setPage(self, page):
    self.currentPage = page

  def setParser(self, parser='lxml'):
    self.pageParser = BeautifulSoup(self.currentPage.content, parser)

  def parseJobListings(self):
    pass

  def parseJobListingInfo(self, pageURL):
    jobListingPage = self.getPage(pageURL)

    if jobListingPage is not None:
      self.setPage(jobListingPage)
      self.setParser()

      self.jobListing = JobListing()