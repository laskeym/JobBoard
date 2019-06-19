# Job Board

Job Board is a web application with the core functionality of aggregating job listings across various sites.  This task is accomplished by using a web scraping combination of requests and BeautifulSoup4.

Currently the application only scrapes from StackOverflow and Monster, but is tailored to expand to other websites.

## TODO

* ~~Add a job date sort feature for job listings.  We can either take advantage of certain sites "sort" feature itself or just grab the results of a basic search and sort the result set.~~
* Refactor and clean up code.  Make the code PEP8 compliant.
* ~~Implement error handling for response pages with a status code != 200~~
* ~~Expand basic UI a bit.~~
* Implement multiprocessing

## Possible Features to Implement

* ~~Might nix the whole job description & company url idea.  Have the scraper parse the job listings page and not the individual pages themselves.~~
* A job consolidation pipeline.  This isn't neccesarily true for SO and Monster, but some job sites have overlapping postings.  For example, Indeed and Glassdoor/Dice/ect.  If this occurs, then this feature should be implemented so there are no double postings.

## Issues

* Indeed & LinkedIn Jobs parser.  These two parsers were implemented before, but both sites have scrape bot detection.  I tried implementing a rotating proxy address solution, but to no avail.  We could either attempt a rotating VPN connection, add some delay between requests(I'd rather not do due to speed being a variable), or trying the Selenium headless browser approach.