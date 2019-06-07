from unittest.mock import patch
import pytest

from job_board.resources.JobParsers.JobSiteParser import JobSiteParser
from job_board.resources.Error import ResponseNotOKError

mockURL = 'https://www.indeed.com'

@pytest.fixture
def job_site_parser():
  """
  Set up an instance of the JobSiteParser class
  """
  jobSiteParser = JobSiteParser()

  return jobSiteParser

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_getPage_function_OKResponse(mock_get, job_site_parser):
  mock_get.return_value.ok = True

  page = job_site_parser.getPage(mockURL)

  assert page is not None

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_getPage_function_notOKResponse(mock_get, job_site_parser):
  mock_get.return_value.ok = False
  mock_get.return_value.status_code = 404

  with pytest.raises(ResponseNotOKError) as err:
    page = job_site_parser.getPage(mockURL)

  assert err.errisinstance(ResponseNotOKError)
  assert err.value.status_code == 404

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_setPage_function_page_set(mock_get, job_site_parser):
  mock_get.return_value.ok = True

  page = job_site_parser.getPage(mockURL)
  job_site_parser.setPage(page)

  assert job_site_parser.currentPage is not None

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_setPage_function_page_not_set(mock_get, job_site_parser):
  mock_get.return_value.ok = True

  page = job_site_parser.getPage(mockURL)

  assert job_site_parser.currentPage is None

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_page_content(mock_get, job_site_parser):
  """
  Test getPage() page content.
  """
  mock_get.return_value.ok = True
  mock_get.return_value.content = bytes(
      """
      <div>
        <h1>Software Developer</h1>
      </div>
    """
  , 'UTF-8')

  page = job_site_parser.getPage(mockURL)

  assert page.content is not None
  assert isinstance(page.content, bytes)

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_setParser_function_page_not_set(mock_get, job_site_parser):
  """
  Test setParser() function when JobSiteParser.currentPage is not set.  This should throw an AttributeError.
  """
  mock_get.return_value.ok = True

  page = job_site_parser.getPage(mockURL)

  with pytest.raises(AttributeError) as err:
    job_site_parser.setParser()

  assert job_site_parser.pageParser is None
  assert err.exconly() == 'AttributeError: \'NoneType\' object has no attribute \'content\'' 
  assert err.errisinstance(AttributeError)

@patch('job_board.resources.JobParsers.JobSiteParser.requests.get')
def test_setParser_function_page_set(mock_get, job_site_parser):
  """
  Test setParser() function when JobSiteParser.currentPage is not set.  This should throw an AttributeError.
  """
  mock_get.return_value.ok = True
  mock_get.return_value.content = bytes(
    """
    <div>
      <h1>Software Developer</h1>
    </div>
  """
  , 'UTF-8')

  page = job_site_parser.getPage(mockURL)
  job_site_parser.setPage(page)
  job_site_parser.setParser()

  assert job_site_parser.pageParser is not None

  pageExtract = job_site_parser.pageParser.find('h1')

  assert pageExtract is not None