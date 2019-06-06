import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

from urllib.parse import urljoin

from unittest.mock import patch
import pytest

from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobParsers.StackOverFlowParser import StackOverflowParser

from tests.resources.MockResponse import mocked_requests_get


mockJobListingURL = 'https://www.stackoverflow.com'

@pytest.fixture
def stack_overflow_parser():
  query = JobSearchQuery('Software Developer', 'Fairfield, NJ')

  stackOverflowParser = StackOverflowParser(query)

  return stackOverflowParser

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_parse_job_listing_info(mock_get, stack_overflow_parser):
  mock_get.return_value = mocked_requests_get('https://www.stackoverflow.com/jobs')

  jobListing = stack_overflow_parser.parseJobListingInfo(mockJobListingURL)

  assert jobListing.jobTitle == 'Software Developer'
  assert jobListing.companyName == 'ABC Corp.'
  assert jobListing.companyURL == 'https://www.abcCorp.org'
  assert jobListing.jobDescription != ''
  
@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_get_job_listings_mock(mock_get, stack_overflow_parser):
  mock_get.return_value = mocked_requests_get(urljoin(mockJobListingURL, 'jobs'))

  
  jobListingsPage = mocked_requests_get(mockJobListingURL)
  stack_overflow_parser.setPage(jobListingsPage)
  stack_overflow_parser.setParser()
  stack_overflow_parser.parseJobListings()

  assert len(stack_overflow_parser.jobListings) == 3
  assert stack_overflow_parser.jobListings[0].jobTitle is not None

@pytest.mark.live
def test_get_job_listings_live():
  # print('\n')
  # print('LIVE TEST: StackOverflow connectivity and job search')

  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  sop = StackOverflowParser(jsq)

  StackOverflowPageResponse = sop.getPage(sop.searchURL, sop.urlParams)
  sop.setPage(StackOverflowPageResponse)
  sop.setParser()

  sop.getJobListings()

  assert len(sop.jobListings) > 0

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_time_parser(mock_get, stack_overflow_parser):
  # TODO:
    # Account for 'yesterday'

  mock_get.return_value = mocked_requests_get(mockJobListingURL)

  jobListingsPage = stack_overflow_parser.getPage(mockJobListingURL)
  stack_overflow_parser.setPage(jobListingsPage)
  stack_overflow_parser.setParser()

  postDate = stack_overflow_parser.pageParser.find_all('span', attrs={'class': 'ps-absolute pt2 r0 fc-black-500 fs-body1 pr12 t32'})

  pattern = r'(\d+)\w{1}'
  pattern2 = '(\d+)'

  for date in postDate:
    dt = re.search(pattern, date.text)
    dt = re.split(pattern2, dt.group(0))
    dt = list(filter(None, dt))

    dateIntervalMapping = {
      'h': 'hours',
      'd': 'days',
      'w': 'weeks',
      'm': 'months'
    }

    dtInterval = dateIntervalMapping[dt[1]]
    dtDict = {
      dtInterval: -int(dt[0])
    }

    dt = datetime.now() + relativedelta(**dtDict)

  
  strftimePattern = "%Y-%m-%d %H:%M%S"
  assert isinstance(dt, datetime)
  assert dt.strftime(strftimePattern) == (datetime.now() + relativedelta(hours=-15)).strftime(strftimePattern)