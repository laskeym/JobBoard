==========
Job Board
==========

Summary
========

This is a rewrite of my original code when I first started back as a Software Developer at BenefitPlan Manager.

The goal of this project is to use a web scraping library to scrape the latest job postings across multiple job posting sites.  These sites include Indeed, SimplyHired, Dice, as well as others if possible.  A few things to clear up:

1.  The reason we are using a web scraping library is because we would need to go through the companies themselves to use their APIs, IF they have APIs.
2.  The reason this project is being redone is because I am now...three years into my career from the time I worked on this.  I also just finished reading Clean Code by Robert Martin and want to take on a small project that will allow me to practice these principles.
3.  The job sites listed are just a base.  I would like to expand on them further, but need to see how the project progresses with simple ones at first.

Library Requirements
======================

* Flask v1.0.3
* Requests v2.22.0
* Beautiful Soup 4 v4.7.1
* PyTest v4.5.0

Project Functions
===================

The main function of this project is to scrape data off of the job listing sites.  Once we get this working we will add more functionality.