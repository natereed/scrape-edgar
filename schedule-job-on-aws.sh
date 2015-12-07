#!/usr/bin/env bash
curl http://ec2-54-183-74-84.us-west-1.compute.amazonaws.com:6800/schedule.json -d project=ScrapeEdgar -d spider=edgar -d input_file=https://s3-us-west-1.amazonaws.com/edgar-crawler/sp500_companies_cleaned.csv

