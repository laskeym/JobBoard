from flask import Flask, render_template, request

from job_board.resources.JobSearchQuery import JobSearchQuery
from job_board.resources.JobParsers.StackOverFlowParser import StackOverflowParser
from job_board.resources.JobParsers.MonsterParser import MonsterParser


app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
  query = request.form.get('query')
  location = request.form.get('location')
  jobListings = []

  jobSearchQuery = JobSearchQuery(query, location)

  stackOverflow = StackOverflowParser(jobSearchQuery)
  stackOverflowPage = stackOverflow.getPage(stackOverflow.searchURL, stackOverflow.urlParams)
  stackOverflow.setPage(stackOverflowPage)
  stackOverflow.setParser()
  
  stackOverflow.getJobListings()
  jobListings.extend(stackOverflow.jobListings)

  monster = MonsterParser(jobSearchQuery)
  jobListings.extend(monster.getJobListings())

  return render_template('search_results.html', jobListings=jobListings)