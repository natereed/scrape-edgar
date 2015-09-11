## Basic usage

Usage:

  scrapy crawl edgar -a -t csv --logfile scrapy.log

The output will be written to the bucket specified by SCRAPY_FEED_URI as items.json.

## Automated tests

To run the full suite of tests:

  ./test.sh

## Scrapyd

Scrapyd is a daemon that provides a REST interface for deploying spiders, starting crawls and getting job status remotely. This provides an ideal interface for
controlling jobs remotely.

Start the server with 'scrapyd', or as a service with 'sudo service scrapyd start'.

To deploy to Scrapyd:

  scrapyd-deploy localhost -p ScrapeEdgar

This creates a spider called "edgar". Now that it's deployed, we can schedule a job:

  curl http://localhost:6800/schedule.json -d project=ScrapeEdgar -d spider=edgar -d input_file=companies.csv

For convenience, a script (schedule-job-on-aws.sh) is provided for scheduling a crawl on AWS.

## Installation on Amazon EC2 / Ubuntu

This section defines how to install scrapyd on an EC2 instance. Scrapyd is the service that runs as a daemon and accepts Scrapy crawl jobs.

Scrapy and scrapyd can be installed using the Python package management system (pip), but use the OS package management system to install scrapyd with
startup ("upstart") script support.

Use: sudo apt-get install scrapyd

