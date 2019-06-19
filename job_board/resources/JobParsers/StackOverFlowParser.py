import re
import datetime
from dateutil.relativedelta import relativedelta

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.JobSiteParser import JobSiteParser
from job_board.resources.Error import ResponseNotOKError
from job_board.utilities.dateParser import dateParserStackOverflow


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

    postDateRaw = jobHeaderInfo.find('span', attrs={'class': 'fc-black-500'}).text
    jobListingObj.postDate = dateParserStackOverflow(postDateRaw)

    return jobListingObj
