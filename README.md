## Installation on Amazon EC2 / Ubuntu

This section defines how to install scrapyd on an EC2 instance. Scrapyd is the service that runs as a daemon and accepts Scrapy crawl jobs.

Scrapy and scrapyd are installed using the Python package management system (pip).

Installing these packages will also install a number of dependencies, but some of the scrapy dependencies might need to be installed manually. I had
to install a few additional packages, as shown in the install steps below:

    sudo pip install Scrapy
    sudo pip install scrapyd
    sudo pip install characteristic
    sudo pip install pyasn1-modules

In addition, an init script wrapper is installed in /etc/init.d/scrapyd. Do the following:

   sudo cp ubuntu-init-scrapy.sh /etc/init.d/scrapyd

Configuration is defined in /etc/scrapyd/scrapyd.conf. Copy the provided scrapyd configuration:

    sudo mkdir /etc/scrapyd
    sudo cp scrapyd.conf /etc/scrapyd

The init.d service depends on some host OS environment variables that enable the interface with S3. The script
'defaults-scrapyd' contains a template. Fill these variables in with the path to the AWS S3 bucket where scraped items
 should be written, and replace the AWS credentials.

Then, copy the file to the appropriate location:
    sudo cp defaults-scrapyd /etc/default/scrapyd

## Output

ScrapeEdgar is configured to export the feed to an S3 bucket via the FEED_URI variable defined in the settings module.
The AWS credentials should also be set as environment variables.

## Environment variables

For the Linux service (/etc/init.d/scrapyd), the default environment variables are found in /etc/default/set-defaults-scrapyd.

For running locally, simply edit set-defaults-scrapyd and execute:

    set-defaults-scrapyd.sh

This sets the SCRAPY_FEED_URI, SCRAPY_AWS_SECRET_ACCESS_KEY and SCRAPY_AWS_ACCESS_KEY_ID variables, which are needed for
configuring the S3 feed export.

## Basic usage

Usage:

  scrapy crawl edgar -a -t csv --logfile scrapy.log

The output will be written to the bucket specified by SCRAPY_FEED_URI as items.json.

## Scrapyd

Scrapyd is a daemon that provides a REST interface for deploying spiders, starting crawls and getting job status remotely. This provides an ideal interface for
controlling jobs remotely.

Start the server with 'scrapyd', or as a service with 'sudo service scrapyd start'.

To deploy to Scrapyd:

  scrapyd-deploy localhost -p ScrapeEdgar

This creates a spider called "edgar". Now that it's deployed, we can schedule a job:

  curl http://localhost:6800/schedule.json -d project=ScrapeEdgar -d spider=edgar -d input_file=companies.csv

For convenience, a script (schedule-job-on-aws.sh) is provided for scheduling a crawl on AWS.

## Automated tests

To run the full suite of tests:

  ./test.sh


