import re
import datetime
from dateutil.relativedelta import relativedelta
from urllib.parse import urljoin

from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.JobSiteParser import JobSiteParser
from job_board.resources.Error import ResponseNotOKError

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
    self.setUpPage()
    jobListingsContent = self.pageParser.find_all('section', attrs={'class': 'card-content', 'data-jobid': re.compile(r'(\d+)')})
    self.parseJobListings(jobListingsContent)

    return self.jobListings

  def setUpPage(self):
    try:
      jobListingsPage = self.getPage(self.searchURL, self.urlParams)
    except ResponseNotOKError as err:
      err.printError()
      return 0
    
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
    jobListingObj.postDate = self.timeParser(postDateRaw)

    return jobListingObj

  def timeParser(self, timeString):
    datePattern = r'((\d+) day(s)?|today)'
    dateSearch = re.search(datePattern, timeString)

    dateListRaw = re.split('(\d+)', dateSearch.group(0))
    dateListRaw = list(filter(None, dateListRaw))

    if dateListRaw[0] == 'today':
      dt = datetime.date.today()
    else:
      if dateListRaw[1].strip() == 'day':
        dateListRaw[1] = 'days'

      dateDict = {
        dateListRaw[1].strip(): -int(dateListRaw[0])
      }
      dt = datetime.date.today() + relativedelta(**dateDict)

    return dt