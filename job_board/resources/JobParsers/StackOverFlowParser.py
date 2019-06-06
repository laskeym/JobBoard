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
    jobListingsPage = self.getPage(self.searchURL, self.urlParams)
    self.setPage(jobListingsPage)
    self.setParser()
    self.parseJobListings()

    return self.jobListings

  def parseJobListings(self):
    jobListingsURL = self.pageParser.find_all('a', attrs={'class': 's-link s-link__visited'})
    jobListingsPostDate = self.pageParser.find_all('span', attrs={'class': 'ps-absolute pt2 r0 fc-black-500 fs-body1 pr12 t32'})

    jobListings = list(zip(jobListingsURL, jobListingsPostDate))

    for jobListing in jobListings:
      jobListingObj = self.parseJobListingInfo(urljoin(self.URL, jobListing[0]['href']))
      jobListingObj.postDate = self.timeParser(jobListing[1].text)
      self.jobListings.append(jobListingObj)

  def parseJobListingInfo(self, pageURL):
    super().parseJobListingInfo(pageURL) 

    self.jobListing.jobTitle = self.pageParser.find('a', attrs={'class': 'fc-black-900'}).text
    self.jobListing.jobURL = pageURL

    companyInfo = self.pageParser.find('a', attrs={'class': ['fc-black-700', 'fc-black-800']})
    self.jobListing.companyName = companyInfo.text
    self.jobListing.companyURL = companyInfo.get('href')

    jobDescriptionExtract = self.pageParser.find('div', {'id': 'overview-items'})
    jobDescriptionExtract = jobDescriptionExtract.find_all('section')[2].text
    self.jobListing.jobDescription = jobDescriptionExtract
    
    return self.jobListing

  def timeParser(self, timeString):
    """
    Convert a time string such as '12d ago' to a datetime object
    """
    # print(timeString)

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