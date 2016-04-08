#curl http://localhost:6800/schedule.json -d project=ScrapeEdgar -d spider=edgar -d input_file=https://s3-us-west-1.amazonaws.com/edgar-crawler/sp500-companies.csv -d FEED_URI=s3://edgar-crawler/items.csv -d SCRAPY_AWS_ACCESS_KEY_ID=AKIAI4BK4C7PI5U4RFPA -d SCRAPY_AWS_SECRET_ACCESS_KEY=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 -d FEED_FORMAT=csv
curl http://localhost:6800/schedule.json -d project=ScrapeEdgar -d spider=edgar -d input_file=companies-awstest.csv -d FEED_URI=s3://edgar-crawler/items.csv -d SCRAPY_AWS_ACCESS_KEY_ID=AKIAI4BK4C7PI5U4RFPA -d SCRAPY_AWS_SECRET_ACCESS_KEY=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 -d FEED_FORMAT=csv



