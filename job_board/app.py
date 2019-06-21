from flask import Flask, render_template, request, url_for
from paginate import Page

from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobParsers.StackOverFlowParser import StackOverflowParser
from job_board.resources.JobParsers.MonsterParser import MonsterParser
from job_board.resources.Error import ResponseNotOKError

app = Flask(__name__)

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

  stackOverflow = StackOverflowParser(jobSearchQuery)
  try:
    jobListings.extend(stackOverflow.getJobListings())
  except ResponseNotOKError as err:
    errors.append(err.printError)

  monster = MonsterParser(jobSearchQuery)
  try:
    jobListings.extend(monster.getJobListings())
  except ResponseNotOKError as err:
    errors.append(err.printError)

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