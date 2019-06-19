import re
import datetime
from dateutil.relativedelta import relativedelta
from urllib.parse import urljoin

from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.JobSiteParser import JobSiteParser

from job_board.utilities.dateParser import dateParserMonster


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
    self.setUpPage()
    jobListingsContent = self.pageParser.find_all('section', attrs={'class': 'card-content', 'data-jobid': re.compile(r'(\d+)')})
    self.parseJobListings(jobListingsContent)

    return self.jobListings

  def setUpPage(self):
    jobListingsPage = self.getPage(self.searchURL, self.urlParams)
    self.setPage(jobListingsPage)
    self.setParser()

  def parseJobListings(self, jobListings):
    for jobListing in jobListings:
      self.jobListings.append(self.createJobListing(jobListing))

  def createJobListing(self, jobListing):
    jobListingObj = JobListing()

    jobListingObj.jobTitle = jobListing.find('a').text
    jobListingObj.jobURL = jobListing.find('a').get('href')
    jobListingObj.companyName = jobListing.find('div', attrs={'class': 'company'}).text.strip()
    jobListingObj.jobLocation = jobListing.find('div', attrs={'class': 'location'}).text.strip()

    postDateRaw = jobListing.find('time').text
    jobListingObj.postDate = dateParserMonster(postDateRaw)

    return jobListingObj