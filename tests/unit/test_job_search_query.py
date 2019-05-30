import pytest

from job_board.resources.JobSearchQuery import JobSearchQuery

def test_job_search_query_instantiation_no_params():
  with pytest.raises(TypeError) as err:
    jsq = JobSearchQuery()

  assert err.exconly() == 'TypeError: __init__() missing 2 required positional arguments: \'jobTitle\' and \'jobLocation\'' 
  assert err.errisinstance(TypeError)

def test_job_search_query():
  jsq = JobSearchQuery('Software Developer', 'New York, NY')

  assert jsq.getJobTitle() == 'Software Developer'
  assert jsq.getJobLocation() == 'New York, NY'
  