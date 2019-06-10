import re
import datetime
from dateutil.relativedelta import relativedelta

from bs4 import BeautifulSoup

from urllib.parse import urljoin

from unittest.mock import patch
import pytest

from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobListing import JobListing
from job_board.resources.JobParsers.StackOverFlowParser import StackOverflowParser
from job_board.utilities.dateParser import dateParserStackOverflow

from tests.resources.MockResponse import mocked_requests_get


mockJobListingURL = 'https://www.stackoverflow.com'

@pytest.fixture
def stack_overflow_parser():
  query = JobSearchQuery('Software Developer', 'Fairfield, NJ')

  stackOverflowParser = StackOverflowParser(query)

  return stackOverflowParser
  
def test_create_job_listing(stack_overflow_parser):
  mockJobListingPage = mocked_requests_get(urljoin(mockJobListingURL, 'jobs'))

  jobListingParser = BeautifulSoup(mockJobListingPage.content, 'lxml')
  jobListing = stack_overflow_parser.createJobListing(jobListingParser)

  assert isinstance(jobListing, JobListing)
  assert jobListing.jobTitle == 'Software Developer'
  assert jobListing.jobURL == mockJobListingURL
  assert jobListing.companyName == 'ABC Company'
  assert jobListing.jobLocation == 'New York, NY'

  datetimePattern = "%Y-%m-%d"
  assert jobListing.postDate.strftime(datetimePattern) == (datetime.date.today() + relativedelta(days=-1)).strftime(datetimePattern)

def test_parse_job_listings(stack_overflow_parser):
  mockJobListingsPage = mocked_requests_get(mockJobListingURL)

  jobListingsParser = BeautifulSoup(mockJobListingsPage.content, 'lxml')
  jobListings = jobListingsParser.find_all('div', attrs={'class': '-job-summary'})
  stack_overflow_parser.parseJobListings(jobListings)

  assert len(stack_overflow_parser.jobListings) == 3

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_get_job_listings(mock_get, stack_overflow_parser):
  mock_get.return_value = mocked_requests_get(mockJobListingURL)

  jobListings = stack_overflow_parser.getJobListings()

  assert len(jobListings) == 3

@pytest.mark.live
def test_get_job_listings_live(stack_overflow_parser):
  print('\n')
  print('-'*41)
  print('STACKOVERFLOW GET JOB LISTINGS LIVE TEST')
  print('-'*41)

  stack_overflow_parser.getJobListings()

  assert len(stack_overflow_parser.jobListings) > 0
  
def test_time_parser(stack_overflow_parser):
  mockJobListingPage = mocked_requests_get(urljoin(mockJobListingURL, 'jobs'))
  
  jobListingParser = BeautifulSoup(mockJobListingPage.content, 'lxml')
  jobHeaderInfo = jobListingParser.find('div', attrs={'class': '-title'})

  postedDateRaw = jobHeaderInfo.find('span', attrs={'class': 'fc-black-500'}).text
  parsedTime = dateParserStackOverflow(postedDateRaw)

  datetimePattern = "%Y-%m-%d %H:%M:%S"
  assert parsedTime.strftime(datetimePattern) == (datetime.date.today() + relativedelta(days=-1)).strftime(datetimePattern)
