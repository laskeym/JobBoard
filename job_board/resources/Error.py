class Error(Exception):
  """Base class for exceptions in this module"""
  pass

class ResponseNotOKError(Error):
  def __init__(self, pageURL, status_code):
    self.pageURL = pageURL
    self.status_code = status_code
    self.message = None

  def printError(self):
    self.message = 'Page \'{url}\' returned with a status code of {status_code}!'