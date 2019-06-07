import re
import datetime
from dateutil.relativedelta import relativedelta

from bs4 import BeautifulSoup

from urllib.parse import urljoin

from unittest.mock import patch
import pytest

from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.MonsterParser import MonsterParser

from tests.resources.MockResponse import mocked_requests_get


mockJobListingURL = 'https://www.monster.com'

@pytest.fixture
def monster_parser():
  query = JobSearchQuery('Software Developer', 'Fairfield, NJ')

  monsterParser = MonsterParser(query)

  return monsterParser

def test_create_job_listing(monster_parser):
  mockJobListingPage = mocked_requests_get(urljoin(mockJobListingURL, 'jobs/search'))

  jobListingParser = BeautifulSoup(mockJobListingPage.content, 'lxml')

  jobListing = monster_parser.createJobListing(jobListingParser)

  assert isinstance(jobListing, JobListing)
  assert jobListing.jobTitle == 'AWS Architect'
  assert jobListing.jobURL == mockJobListingURL
  assert jobListing.companyName == 'Tech Solutions Inc'
  assert jobListing.jobLocation == 'Parsippany, NJ'

  assert jobListing.postDate == datetime.date.today() + relativedelta(days=-10)

def test_parse_job_listings(monster_parser):
  mockJobListingsPage = mocked_requests_get(mockJobListingURL)

  jobListingsParser = BeautifulSoup(mockJobListingsPage.content, 'lxml')
  jobListings = jobListingsParser.find_all('section', attrs={'class': 'card-content'})
  monster_parser.parseJobListings(jobListings)

  assert len(monster_parser.jobListings) == 4

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_get_job_listings(mock_get, monster_parser):
  mock_get.return_value = mocked_requests_get(mockJobListingURL)

  jobListings = monster_parser.getJobListings()

  assert len(jobListings) == 4

@pytest.mark.live
def test_get_job_listings_live(monster_parser):
  print('\n')
  print('-'*35)
  print('MONSTER GET JOB LISTINGS LIVE TEST')
  print('-'*35)
  monster_parser.getJobListings()

  assert len(monster_parser.jobListings) > 0

def test_time_parser(monster_parser):
  mockJobListingPage = mocked_requests_get(urljoin(mockJobListingURL, 'jobs/search'))
  
  jobListingParser = BeautifulSoup(mockJobListingPage.content, 'lxml')

  postDateRaw = jobListingParser.find('time').text
  parsedDate = monster_parser.timeParser(postDateRaw)

  assert parsedDate == datetime.date.today() + relativedelta(days=-10)