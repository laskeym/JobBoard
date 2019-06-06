# Job Board

Job Board is a web application with the core functionality of aggregating job listings across various sites.  This task is accomplished by using a web scraping combination of requests and BeautifulSoup4.

Currently the application only scrapes from StackOverflow and Monster, but is tailored to expand to other websites.

## TODO

* Add a job date sort feature for job listings.  We can either take advantage of certain sites "sort" feature itself or just grab the results of a basic search and sort the result set.
* Refactor and clean up code.
* Expand basic UI a bit.
* Implement multiprocessing