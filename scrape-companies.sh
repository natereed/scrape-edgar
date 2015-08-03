mkdir runs/07302015
scrapy crawl edgar -a input_file=companies-chunk1.csv -o runs/07302015/items1.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk2.csv -o runs/07302015/items2.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk3.csv -o runs/07302015/items3.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk4.csv -o runs/07302015/items4.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk5.csv -o runs/07302015/items5.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk6.csv -o runs/07302015/items6.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk7.csv -o runs/07302015/items7.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk8.csv -o runs/07302015/items8.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk9.csv -o runs/07302015/items9.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk10.csv -o runs/07302015/items10.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk11.csv -o runs/07302015/items11.csv -t csv --logfile scrapy.log &
scrapy crawl edgar -a input_file=companies-chunk12.csv -o runs/07302015/items12.csv -t csv --logfile scrapy.log &

