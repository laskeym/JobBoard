import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.JobSiteParser import JobSiteParser


class StackOverflowParser(JobSiteParser):
  def __init__(self, jobSearchQuery):
    super(StackOverflowParser, self).__init__()

    self.URL = 'https://stackoverflow.com'
    self.urlParams = {
      'q': jobSearchQuery.getJobTitle(),
      'l': jobSearchQuery.getJobLocation()
    }
    self.jobListings = []

  @property
  def searchURL(self):
    return urljoin(self.URL, 'jobs')

  def getJobListings(self):
    self.setUpPage()
    jobListingsContent = self.pageParser.find_all('div', attrs={'class': '-job-summary'})

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

    jobHeaderInfo = jobListing.find('div', attrs={'class': '-title'})
    jobListingObj.jobTitle = jobHeaderInfo.find('a').text
    jobListingObj.jobURL = urljoin(self.URL, jobHeaderInfo.find('a').get('href'))

    secondaryInfo = jobListing.find('div', attrs={'class': '-company'})
    jobListingObj.companyName = secondaryInfo.find('span').text
    jobListingObj.jobLocation = secondaryInfo.find('span', attrs={'class': 'fc-black-500'}).text

    postedDateRaw = jobHeaderInfo.find('span', attrs={'class': 'fc-black-500'}).text
    jobListingObj.postedDate = self.timeParser(postedDateRaw)

    return jobListingObj

  # Might break off into its own class since multiple parsers need this and are special cases. 
  def timeParser(self, timeString):
    """
    Convert a time string such as '12d ago' to a datetime object
    """
    dateIntervalMapping = {
      'h': 'hours',
      'd': 'days',
      'w': 'weeks',
      'm': 'months'
    }

    dtPattern1 = '(\d+)\w{1}'
    dtPattern2 = '(\d+)'

    dt = re.search(dtPattern1, timeString)
    dt = re.split(dtPattern2, dt.group(0))
    dt = list(filter(None, dt))

    dtInterval = dateIntervalMapping[dt[1]]
    dtDict = {
      dtInterval: -int(dt[0])
    }

    dt = datetime.now() + relativedelta(**dtDict)

    return dt