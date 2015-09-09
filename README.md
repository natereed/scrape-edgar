## Initial configuration: Writing to S3

ScrapeEdgar is configured to export the feed to an S3 bucket via the FEED_URI variable defined in the settings module.
The AWS credentials should also be set as environment variables. For convenience, a setenv.sh script is provided.
Replace the values of these variables with the actual values, then source the script:

  source setenv.sh

This sets the SCRAPY_FEED_URI, SCRAPY_AWS_SECRET_ACCESS_KEY and SCRAPY_AWS_ACCESS_KEY_ID variables.

## Basic usage

Usage:

  scrapy crawl edgar -a -t csv --logfile scrapy.log

The output will be written to the bucket specified by SCRAPY_FEED_URI as items.json.

## Scrapyd

Scrapyd is a daemon that provides a REST interface for deploying spiders, starting crawls and getting job status remotely. This provides an ideal interface for
controlling jobs remotely.

Start the server with 'scrapyd'.

To deploy to Scrapyd:

  scrapyd-deploy localhost -p ScrapeEdgar

This creates a spider called "edgar". Now that it's deployed, we can schedule a job:

  curl http://localhost:6800/schedule.json -d project=ScrapeEdgar -d spider=edgar -d input_file=companies.csv

## Automated tests

To run the full suite of tests:

  ./test.sh


