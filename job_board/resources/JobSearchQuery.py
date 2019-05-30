class JobSearchQuery:
  def __init__(self, jobTitle, jobLocation):
    self._jobTitle = jobTitle
    self._jobLocation = jobLocation 

  def displayJobSearchQuery(self):
    message = 'Searching for {jT} jobs in {jL}'.format(jT=self._jobTitle, jL=self._jobLocation)

  def getJobTitle(self):
    return self._jobTitle

  def getJobLocation(self):
    return self._jobLocation