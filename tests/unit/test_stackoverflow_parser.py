import os
import random

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
def test_get_job_listing_info(mock_get, stack_overflow_parser):
  mock_get.return_value = mocked_requests_get('https://www.stackoverflow.com/jobs')

  jobListing = stack_overflow_parser.getJobListingInfo(mockJobListingURL)

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
  stack_overflow_parser.getJobListings()

  assert len(stack_overflow_parser.jobListings) == 3
  assert stack_overflow_parser.jobListings[0].jobTitle is not None

@pytest.mark.live
def test_get_job_listings_live():
  print('\n')
  print('LIVE TEST: StackOverflow connectivity and job search')

  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  sop = StackOverflowParser(jsq)

  StackOverflowPageResponse = sop.getPage(sop.searchURL, sop.urlParams)
  sop.setPage(StackOverflowPageResponse)
  sop.setParser()

  sop.getJobListings()

  assert len(sop.jobListings) > 0