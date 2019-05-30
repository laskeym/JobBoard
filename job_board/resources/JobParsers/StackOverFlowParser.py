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
    jobListings = self.pageParser.find_all('a', attrs={'class': 's-link s-link__visited'})

    for jobListing in jobListings:
      jobListing = self.getJobListingInfo(urljoin(self.URL, jobListing['href']))
      self.jobListings.append(jobListing)

  def getJobListingInfo(self, pageURL):
    jobListingPage = self.getPage(pageURL)
    self.setPage(jobListingPage)
    self.setParser()

    jobListing = JobListing()
    jobListing.jobTitle = self.pageParser.find('a', attrs={'class': 'fc-black-900'}).text
    jobListing.jobURL = pageURL

    companyInfo = self.pageParser.find('a', attrs={'class': ['fc-black-700', 'fc-black-800']})
    jobListing.companyName = companyInfo.text
    jobListing.companyURL = companyInfo.get('href')

    jobDescriptionExtract = self.pageParser.find('div', {'id': 'overview-items'})
    jobDescriptionExtract = jobDescriptionExtract.find_all('section')[2].text
    jobListing.jobDescription = jobDescriptionExtract
    
    return jobListing