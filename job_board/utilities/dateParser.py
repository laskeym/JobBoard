import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


def dateParserMonster(dateString):
  datePattern = r'((\d+) day(s)?|today)'
  dateSearch = re.search(datePattern, dateString)

  postDate = parseDateMonster(dateSearch.group(0))

  return postDate

def parseDateMonster(dateExtract):
  dateList = re.split('(\d+)', dateExtract)
  dateList = list(filter(None, dateList))

  parsedDate = createDateMonster(dateList)

  return parsedDate

def createDateMonster(parsedDateList):
  """
  Ex of dateDict:

  {
    'days': -5
  }
  """
  if parsedDateList[0] == 'today':
    dt = datetime.now()
  else:
    if parsedDateList[1].strip() == 'day':
      parsedDateList[1] = 'days'

    dateDict = {
      parsedDateList[1].strip(): -int(parsedDateList[0])
    }
    dt = datetime.now() + relativedelta(**dateDict)
  
  return dt

def dateParserStackOverflow(dateString):
  datePattern = r'(\d+)\w{1}|yesterday'
  dateSearch = re.search(datePattern, dateString)

  postDate = createDateStackOverflow(dateSearch.group(0))

  return postDate

def createDateStackOverflow(dateExtract):
  """
  Ex of dateDict: 
  {
    'hours': 23
  }
  """
  if dateExtract == 'yesterday':
    dateDict = {
      dateIntervalMappingStackOverflow()['d']: -1
    }
  else:
    dt = re.split(r'(\d+)', dateExtract)
    dt = list(filter(None, dt))

    dateDict = {
      dateIntervalMappingStackOverflow()[dt[1]]: -int(dt[0])
    }

  dt = datetime.now() + relativedelta(**dateDict)

  return dt

def dateIntervalMappingStackOverflow():
  dateIntervalMapping = {
    'h': 'hours',
    'd': 'days',
    'w': 'weeks',
    'm': 'months'
  }

  return dateIntervalMapping