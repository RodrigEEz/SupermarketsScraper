# Supermarket Scraper

Python project that scrapes product prices from websites of paraguayan major supermarket chains.

# How to use

This is an early version of the project. You can enter in marketScraper and look for scraper names, then run this command in the shell

```scrapy crawl 'enter the scraper you want to test here'```

Currently, the data is saved in an example sqlite database. If you want to change the database where information is stored, go to ```marketSpiders/pipelines.py``` and change ```DatabaseInsert``` class.

# Next steps

-Add scrapers for more supermarkets  
-Add menu for executing spiders outside shell  
-Containerize application with Docker
