import re
import datetime
from dateutil.relativedelta import relativedelta

from urllib.parse import urljoin

from unittest.mock import patch
import pytest

from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobParsers.MonsterParser import MonsterParser

from tests.resources.MockResponse import mocked_requests_get


mockJobListingURL = 'https://www.monster.com'

@pytest.fixture
def monster_parser():
  query = JobSearchQuery('Software Developer', 'Fairfield, NJ')

  monsterParser = MonsterParser(query)

  return monsterParser

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_parse_job_listing_info(mock_get, monster_parser):
  mock_get.return_value = mocked_requests_get('https://www.monster.com/jobs/search')

  jobListing = monster_parser.parseJobListingInfo(mockJobListingURL)

  assert jobListing.jobTitle == 'Software Developer'
  assert jobListing.companyName == 'ABC Corp.'
  assert jobListing.companyURL == None # Monster doesn't provide a URL
  assert jobListing.jobDescription != ''
  
@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_parse_job_listings_mock(mock_get, monster_parser):
  mock_get.return_value = mocked_requests_get(urljoin(mockJobListingURL, 'jobs/search'))

  jobListingsPage = mocked_requests_get(mockJobListingURL)
  monster_parser.setPage(jobListingsPage)
  monster_parser.setParser()

  monster_parser.parseJobListings()

  assert len(monster_parser.jobListings) == 4
  assert monster_parser.jobListings[0].jobTitle is not None

def test_get_job_listings_mock():
  pass

@pytest.mark.live
def test_get_job_listings_live(monster_parser):
  print('\n')
  print('LIVE TEST: Monster connectivity and job search')

  monster_parser.getJobListings()

  assert len(monster_parser.jobListings) > 0

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_time_parser(mock_get, monster_parser):
  mock_get.return_value = mocked_requests_get(mockJobListingURL)

  jobListingsPage = monster_parser.getPage(mockJobListingURL)
  monster_parser.setPage(jobListingsPage)
  monster_parser.setParser()

  postDates = monster_parser.pageParser.find_all('time', attrs={'datetime': '2017-05-26T12:00'})

  pattern = r'((\d+) day(s)?|today)'

  for postDate in postDates:
    rx = re.search(pattern, postDate.text)

    x = re.split('(\d+)', rx.group(0))
    x = list(filter(None, x))

    if x[0] == 'today':
      dt = datetime.date.today()
    else:
      if x[1].strip() == 'day':
        x[1] = 'days'

      dtDict = {
        x[1].strip(): -int(x[0])
      }

      dt = datetime.date.today() + relativedelta(**dtDict)

  assert isinstance(dt, datetime.date)
  assert dt == datetime.date.today() + relativedelta(days=-12)