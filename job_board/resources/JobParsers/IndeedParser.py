from urllib.parse import urljoin

from bs4 import BeautifulSoup

from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.JobSiteParser import JobSiteParser


class IndeedParser(JobSiteParser):
  """
  DO NOT USE.  INDEED SITE IS TOO VOLATILE.  SEE getJobListingInfo() FOR MORE INFO.
  """

  def __init__(self, jobSearchQuery):
    super(IndeedParser, self).__init__()

    self.URL = 'https://www.indeed.com/'
    self.urlParams = {
      'q': jobSearchQuery.getJobTitle(),
      'l': jobSearchQuery.getJobLocation()
    }
    self.jobListings = []

  @property
  def searchURL(self):
    return urljoin(self.URL, 'jobs')

  def getJobListings(self):
    jobListings = self.pageParser.find_all('a', attrs={'data-tn-element': 'jobTitle'})

    for jobListing in jobListings:
      jobListing = self.getJobListingInfo(urljoin(self.URL, jobListing['href']))
      self.jobListings.append(jobListing)

  def getJobListingInfo(self, pageURL):
    """
    The function works, but is too volatile.  It seems that the requested pages are picking up on this being a scraper and might be denying access due to too many frequent requests.   
    """
    jobListingPage = self.getPage(pageURL)
    self.setPage(jobListingPage)
    self.setParser()

    jobListing = JobListing()
    jobListing.jobTitle = self.pageParser.find('h3').text
    jobListing.jobURL = pageURL

    companyInfoDiv = self.pageParser.find('div', attrs={'class': 'jobsearch-InlineCompanyRating'})
    companyNameDiv = companyInfoDiv.find('div') if companyInfoDiv is not None else None

    jobListing.companyName = companyNameDiv.text 
    jobListing.companyURL = companyNameDiv.find('a')['href'] 
    jobListing.jobDescription = self.pageParser.find('div', attrs={'id': 'jobDescriptionText'}).text

    return jobListing