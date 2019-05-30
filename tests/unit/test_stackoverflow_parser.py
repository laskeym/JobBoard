from unittest.mock import patch
import pytest

from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobParsers.StackOverFlowParser import StackOverflowParser

def test_get_job_listings():
  jsq = JobSearchQuery('Software Developer', 'Fairfield, NJ')
  sop = StackOverflowParser(jsq)

  StackOverflowPageResponse = sop.getPage(sop.searchURL, sop.urlParams)
  sop.setPage(StackOverflowPageResponse)
  sop.setParser()

  sop.getJobListings()

  assert len(sop.jobListings) > 0
