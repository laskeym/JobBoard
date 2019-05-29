import pytest

from urllib.parse import urljoin

from job_board.app import JobSearchQuery, IndeedParser

def test_indeed_page_connection():
  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  ip = IndeedParser(jsq)

  indeedPageResponse = ip.getPage(ip.searchURL, ip.urlParams)

  assert indeedPageResponse.ok

def test_indeed_search_url():
  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  ip = IndeedParser(jsq)

  assert ip.searchURL == 'https://www.indeed.com/jobs'

def test_set_page():
  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  ip = IndeedParser(jsq)

  indeedPageResponse = ip.getPage(ip.searchURL, ip.urlParams)
  ip.setPage(indeedPageResponse)

  assert ip.currentPage is not None

def test_get_job_listings():
  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  ip = IndeedParser(jsq)

  indeedPageResponse = ip.getPage(ip.searchURL, ip.urlParams)
  ip.setPage(indeedPageResponse)
  ip.setParser()

  jobListings = ip.getJobListings()

  assert len(jobListings) > 0

def test_job_listing_page():
  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  ip = IndeedParser(jsq)

  indeedPageResponse = ip.getPage(ip.searchURL, ip.urlParams)
  ip.setPage(indeedPageResponse)
  ip.setParser()

  jobListings = ip.getJobListings()

  jobListingResponse = ip.getPage(urljoin(ip.URL, jobListings[0]['href']))

  assert jobListingResponse.ok
  
