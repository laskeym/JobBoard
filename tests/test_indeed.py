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

def test_get_job_listing_info():
  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  ip = IndeedParser(jsq)

  indeedPageResponse = ip.getPage(ip.searchURL, ip.urlParams)
  ip.setPage(indeedPageResponse)
  ip.setParser()

  jli = ip.getJobListingInfo('https://www.indeed.com/viewjob?jk=a4ea943f7d845f85&tk=1dc0mhnd70gep002&from=serp&vjs=3')

  assert jli.jobTitle is not None
  assert jli.jobURL is not None
  assert jli.company is not None
  assert jli.companyURL is not None
  assert jli.jobDescription is not None

# def test_get_job_listings():
#   jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
#   ip = IndeedParser(jsq)

#   indeedPageResponse = ip.getPage(ip.searchURL, ip.urlParams)
#   ip.setPage(indeedPageResponse)
#   ip.setParser()

#   ip.getJobListings()

#   assert len(ip.jobListings) > 0

# def test_job_listing_page():
#   jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
#   ip = IndeedParser(jsq)

#   indeedPageResponse = ip.getPage(ip.searchURL, ip.urlParams)
#   ip.setPage(indeedPageResponse)
#   ip.setParser()

#   jobListings = ip.getJobListings()

#   jobListingResponse = ip.getPage(urljoin(ip.URL, jobListings[0]['href']))

#   assert jobListingResponse.ok
