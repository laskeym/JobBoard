import pytest

from job_board import app as job_board


@pytest.fixture
def client():
  job_board.app.config['TESTING'] = True
  client = job_board.app.test_client()

  yield client

def test_home_page(client):
  """Check that home page returns"""
  rv = client.get('/')

  assert b'name="q"' in rv.data

def test_search_page_live(client):
  """
  Should grab all result divs and make sure there is > 0
  """

  rv = client.get('/search', data=dict(
    query='Software Developer',
    location='Fairfield, NJ'
  ))

  assert b'job-listings' in rv.data

def test_search_page_mock():
  """
  Create Mocks for Parser.getJobListings() and check results
  """
  pass

def test_search_page_failed_request():
  """
  Mock Parser.getPage() to return a status code != 200
  """
  pass