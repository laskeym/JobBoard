
###########################################
import os
import random

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
def test_get_job_listing_info(mock_get, monster_parser):
  mock_get.return_value = mocked_requests_get('https://www.monster.com/jobs/search')

  jobListing = monster_parser.getJobListingInfo(mockJobListingURL)

  assert jobListing.jobTitle == 'Software Developer'
  assert jobListing.companyName == 'ABC Corp.'
  assert jobListing.companyURL == None # Monster doesn't provide a URL
  assert jobListing.jobDescription != ''
  
@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_get_job_listings_mock(mock_get, monster_parser):
  mock_get.return_value = mocked_requests_get(urljoin(mockJobListingURL, 'jobs/search'))

  jobListingsPage = mocked_requests_get(mockJobListingURL)
  monster_parser.setPage(jobListingsPage)
  monster_parser.setParser()
  monster_parser.getJobListings()

  assert len(monster_parser.jobListings) == 4
  assert monster_parser.jobListings[0].jobTitle is not None

@pytest.mark.live
def test_get_job_listings_live():
  print('\n')
  print('LIVE TEST: Monster connectivity and job search')

  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  sop = MonsterParser(jsq)

  MonsterPageResponse = sop.getPage(sop.searchURL, sop.urlParams)
  sop.setPage(MonsterPageResponse)
  sop.setParser()

  sop.getJobListings()

  assert len(sop.jobListings) > 0