# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FilingItem(scrapy.Item):
    issuer_name = scrapy.Field()
    issue_name = scrapy.Field()
    document_name = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    cusip = scrapy.Field()
    address = scrapy.Field()
