from flask import Flask, render_template, request, url_for, jsonify
from flask_cors import CORS, cross_origin
from flask_redis import FlaskRedis
from paginate import Page
import requests

from job_board.config import Config
from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobParsers.StackOverFlowParser import StackOverflowParser
from job_board.resources.JobParsers.MonsterParser import MonsterParser
from job_board.resources.Error import ResponseNotOKError
from job_board.utilities.decorators import redisMemoize

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
client = FlaskRedis(app)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/search')
def search():
  query = request.args.get('q')
  location = request.args.get('l')
  page = request.args.get('page', 1)
  jobListings = []
  errors = []

  jobSearchQuery = JobSearchQuery(query, location)
  memoizedGetAllJobListings = redisMemoize(getAllJobListings)
  jobListings = memoizedGetAllJobListings(jobSearchQuery)

  # Sort job listings by post date
  jobListings.sort(key=lambda jobListing: jobListing.postDate, reverse=True)

  jobPaginator = Page(jobListings, page=page)
  pageURL = url_for(
    'search',
    q=query,
    l=location,
    _external=True
  ) + '&page=$page'

  return render_template(
    'search_results.html',
    jobSearchQuery=jobSearchQuery,
    jobListings=jobPaginator,
    pageURL=pageURL,
    errors=errors)

def getAllJobListings(jobSearchQueryObj):
  jobListingResults = []

  stackOverflow = StackOverflowParser(jobSearchQueryObj)
  jobListingResults.extend(stackOverflow.getJobListings())

  monster = MonsterParser(jobSearchQueryObj)
  jobListingResults.extend(monster.getJobListings())

  return jobListingResults

@app.route('/locations', methods=['GET'])
@cross_origin()
def locations():
  locationInput = request.args.get('locationInp')

  return jsonify(getSuggestedLocations(locationInput))

def getSuggestedLocations(locationInput):
  """
  Retrieves location suggestions from HERE Geospatial API.

  Constrained to places in United States of America.
  """

  pageParams = dict(
    app_id=app.config['HERE_APP_ID'],
    app_code=app.config['HERE_APP_CODE'],
    query=locationInput,
    maxresults=20,
    country='USA',
    language='en',
    resultType='areas'
  )
  pageResponse = requests.get(app.config['HERE_API_URL'], params=pageParams)

  if pageResponse.json().get('suggestions'):
    suggestions = pageResponse.json()['suggestions']
    locationsJSON = [sugg for sugg in suggestions if sugg['matchLevel'] == 'city']
    cityStateList = ['{}, {}'.format(loc['address']['city'], loc['address']['state']) for loc in locationsJSON]
    cityStateUniqueList = uniqueList(cityStateList)

    return cityStateUniqueList

  return None

def uniqueList(sequence):
  """
  Converts a list to a unique set of items and preserves order
  """
  seen = set()

  return [item for item in sequence if not (item in seen or seen.add(item))]