
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

def test_get_job_listins_mock():
  pass

@pytest.mark.live
def test_get_job_listings_live(monster_parser):
  print('\n')
  print('LIVE TEST: Monster connectivity and job search')

  monster_parser.getJobListings()

  assert len(monster_parser.jobListings) > 0