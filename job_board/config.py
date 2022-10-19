import os
from urllib.parse import urlparse

class Config(object):
  REDIS_URL = os.environ.get("REDIS_URL")

  HERE_API_URL = 'http://autocomplete.geocoder.api.here.com/6.2/suggest.json'
  HERE_APP_ID = os.environ.get('HERE_APP_ID')
  HERE_APP_CODE = os.environ.get('HERE_APP_CODE')

  CORS_HEADERS = 'Access-Control-Allow-Origin'