from flask import Flask

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

class JobSearchQuery:
  def __init__(self, jobTitle, jobLocation):
    self._jobTitle = jobTitle
    self._jobLocation = jobLocation 

  def displayJobSearchQuery(self):
    message = 'Searching for {jT} jobs in {jL}'.format(jT=self._jobTitle, jL=self._jobLocation)

    print(message)

  def getJobTitle(self):
    return self._jobTitle

  def getJobLocation(self):
    return self._jobLocation


class JobListing:
  def __init__(self):
    self.jobTitle = None
    self.jobURL = None
    self.company = None
    self.companyURL = None
    self.jobDescription = None


class JobSiteParser:
  def __init__(self):
    self.currentPage = None
    self.pageParser = None

  def getPage(self, pageURL, params=None):
    response = requests.get(pageURL, params=params)

    if response.ok:
      return response
    else:
      return None

  def setPage(self, page):
    self.currentPage = page

  def setParser(self, parser='html.parser'):
    self.pageParser = BeautifulSoup(self.currentPage.content, parser)

  def getJobListings(self):
    pass

  def parse(self):
    pass

class IndeedParser(JobSiteParser):
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

      # print(jobListing.text)
      # print(jobListing['href'])
      # print('\n')

    # return jobListings

  def getJobListingInfo(self, pageURL):
    """
    Grab all data from a job listing page
    """
    jobListingResponse = self.getPage(pageURL)
    self.setPage(jobListingResponse)
    self.setParser()

    jobListing = JobListing()
    jobListing.jobTitle = self.pageParser.find('h3').text
    jobListing.jobURL = pageURL

    companyRatingInfoDiv = self.pageParser.find('div', attrs={'class': 'jobsearch-InlineCompanyRating'})
    companyNameDiv = companyRatingInfoDiv.find('div')

    jobListing.company = companyNameDiv.find('a').text
    jobListing.companyURL = companyNameDiv.find('a')['href']
    jobListing.jobDescription = self.pageParser.find('div', attrs={'id': 'jobDescriptionText'}).text

    return jobListing

  def parse(self):
    pass

@app.route('/')
def home():
  jobSearchQuery = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  i = IndeedParser(jobSearchQuery)

  return '<h1>Job Board</h1>'