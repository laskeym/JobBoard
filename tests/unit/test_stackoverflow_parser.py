import random
from urllib.parse import urljoin

# from unittest import mock
from unittest.mock import patch
import pytest

from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobParsers.StackOverFlowParser import StackOverflowParser

mockJobListingURL = 'https://www.stackoverflow.com'
jobTitle = 'Cloud Architect'

mockHTMLJobListingPage = """
  <div>
    <a class="s-link s-link__visited" href="jobs">{jobListingTitle}</a>
  </div>

  <div>
    <a class="s-link s-link__visited" href="jobs">{jobListingTitle}</a>
  </div>
""".format(jobListingTitle=jobTitle)

mockHTMLJobPage = """
  <div>
    <a class="fc-black-900">Software Developer</a>
  </div>

  <div>
    <a class="fc-black-800" href="https://www.abcCorp.org">ABC Corp.</a>
  </div>

  <div id="overview-items">
    <section>
    </section>

    <section>
    </section>

    <section>
      ABC Corp is a world industry leading company that excels at delivering technology solutions to the real estate market!

      ...
    </section>
  </div>
"""

class MockResponse:
  def __init__(self, content, ok):
    self.content = content
    self.ok = ok

def mocked_requests_get(*args, **kwargs):
  if args[0] == mockJobListingURL:
    return MockResponse(mockHTMLJobListingPage, True)
  elif args[0] == urljoin(mockJobListingURL, 'jobs'):
    return MockResponse(mockHTMLJobPage, True)   

@pytest.fixture
def stack_overflow_parser():
  query = JobSearchQuery('Software Developer', 'Fairfield, NJ')

  stackOverflowParser = StackOverflowParser(query)

  return stackOverflowParser

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_get_job_listing_info(mock_get, stack_overflow_parser):
  mock_get.return_value = mocked_requests_get(urljoin(mockJobListingURL, 'jobs'))

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

  assert len(stack_overflow_parser.jobListings) == 2
  assert stack_overflow_parser.jobListings[0].jobTitle is not None

def test_get_job_listings_live():
  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  sop = StackOverflowParser(jsq)

  StackOverflowPageResponse = sop.getPage(sop.searchURL, sop.urlParams)
  sop.setPage(StackOverflowPageResponse)
  sop.setParser()

  sop.getJobListings()

  assert len(sop.jobListings) > 0