from urllib.parse import urljoin
from bs4 import BeautifulSoup

from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.JobSiteParser import JobSiteParser


class LinkedInParser(JobSiteParser):
  def __init__(self, jobSearchQuery):
    super(LinkedInParser, self).__init__()

    self.URL = 'https://www.linkedin.com'
    self.urlParams = {
      'keywords': jobSearchQuery.getJobTitle(),
      'location': jobSearchQuery.getJobLocation()
    }
    self.jobListings = []

  @property
  def searchURL(self):
    return urljoin(self.URL, 'jobs/search')

  def getJobListings(self):
    jobListings = self.pageParser.find_all('a', attrs={'class': 's-link s-link__visited'})

    for jobListing in jobListings:
      jobListing = self.getJobListingInfo(urljoin(self.URL, jobListing['href']))
      self.jobListings.append(jobListing)

  def getJobListingInfo(self, pageURL):
    jobListingPage = self.getPage(pageURL)
    self.setPage(jobListingPage)
    self.setParser()

    jobListing = JobListing()
    
    return jobListing