import os

class Config(object):
  REDIS_URL = 'redis://:4CExG9rB6Xc9KIGSvgyj0fL5qBeR51rq@redis-18223.c10.us-east-1-4.ec2.cloud.redislabs.com:18223/0'

  HERE_API_URL = 'http://autocomplete.geocoder.api.here.com/6.2/suggest.json'
  HERE_APP_ID = os.environ.get('HERE_APP_ID')
  HERE_APP_CODE = os.environ.get('HERE_APP_CODE')

  CORS_HEADERS = 'Access-Control-Allow-Origin'