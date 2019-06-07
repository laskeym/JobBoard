from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re

from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.JobSiteParser import JobSiteParser

#######################################################################
#                               NOTES                                  #
#######################################################################
# We could most likely break out some of the functionlity into         #
# smaller functions                                                    #
#######################################################################

class MonsterParser(JobSiteParser):
  def __init__(self, jobSearchQuery):
    super(MonsterParser, self).__init__()

    self.URL = 'https://www.monster.com'
    self.urlParams = {
      'q': jobSearchQuery.getJobTitle(),
      'where': jobSearchQuery.getJobLocation()
    }
    self.jobListings = []

  @property
  def searchURL(self):
    return urljoin(self.URL, 'jobs/search')

  def getJobListings(self):
    # This could be consolidated to the JobSiteParser parent class by moving URL and urlParms.
    jobListingsPage = self.getPage(self.searchURL, self.urlParams)
    self.setPage(jobListingsPage)
    self.setParser()
    self.parseJobListings()

    return self.jobListings

  def parseJobListings(self):
    jobListings = self.pageParser.find_all('div', attrs={'class': 'summary'})

    for jobListing in jobListings:
      jobListingURL = jobListing.find('a').get('href')
      jobListing = self.parseJobListingInfo(jobListingURL)
      self.jobListings.append(jobListing)

  def parseJobListingInfo(self, pageURL):
    super().parseJobListingInfo(pageURL)

    # This should now be handled by non 202 status code exception
    if self.jobListing:
      infoDiv = self.pageParser.find('h1', attrs={'class': 'title'})
      infoDivCleansed = re.split('at | from', infoDiv.text.strip())

      # The mock getJobListingInfo test fails due to a white space in the job title header.  Look into this more.
      self.jobListing.jobTitle = infoDivCleansed[0].strip()
      self.jobListing.jobURL = pageURL
      self.jobListing.companyName = infoDivCleansed[1]

      self.jobListing.jobDescription = self.pageParser.find('div', attrs={'class': 'details-content'}).text

      return self.jobListing