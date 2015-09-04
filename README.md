## Basic usage

Usage:

scrapy crawl edgar -o items.json --logfile scrapy.log

## Scrapyd

Scrapyd is a daemon that provides a REST interface for deploying spiders, starting crawls and getting job status remotely. This provides an ideal interface for
controlling jobs remotely.

Start the server with 'scrapyd'.

To deploy to Scrapyd:

  scrapyd-deploy localhost -p ScrapeEdgar

This creates a spider called "edgar". Now that it's deployed, we can schedule a job:

  curl http://localhost:6800/schedule.json -d project=ScrapeEdgar -d spider=edgar

## Automated tests

To run the full suite of tests:

./test.sh


