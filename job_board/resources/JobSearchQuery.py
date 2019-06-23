class JobSearchQuery:
  def __init__(self, jobTitle, jobLocation):
    self._jobTitle = jobTitle
    self._jobLocation = jobLocation 

  def __str__(self):
    return '{}({}, {})'.format(
      self.__class__.__name__,
      self.getJobTitle(),
      self.getJobLocation()
    )

  def getJobTitle(self):
    return self._jobTitle

  def getJobLocation(self):
    return self._jobLocation