#!/usr/bin/env bash
curl http://54.215.229.61:6800/schedule.json -d project=ScrapeEdgar -d spider=edgar -d input_file=https://s3-us-west-1.amazonaws.com/edgar-crawler/sp500_companies_cleaned.csv

