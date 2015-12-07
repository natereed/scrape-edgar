# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

class ScrapyItem(scrapy.Item):
    issuer_name = scrapy.Field()
    issue_name = scrapy.Field()
    document_name = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    cusip = scrapy.Field()
    address = scrapy.Field()
    search_term = scrapy.Field()
    document_type = scrapy.Field()
    filing_person = scrapy.Field()

class FilingItem(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def extract_document_name_fields(self, value):
        pat = re.compile(r'([\w\W]+) for ([\w\W]+)$')
        match = pat.search(value)
        document_type = None
        filing_person = None
        if match:
            document_type = match.group(1)
            filing_person = match.group(2)
        return {'document_type' : document_type, 'filing_person' : filing_person}

    def __getitem__(self, key):
        if key == 'document_type' or key == 'filing_person':
            document_name = self.__getitem__('document_name')
            return self.extract_document_name_fields(document_name)[key]
        else:
            return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if key == 'document_name':
            derived_fields = self.extract_document_name_fields(value)
            dict.__setitem__(self, 'document_type', derived_fields['document_type'])
            dict.__setitem__(self, 'filing_person', derived_fields['filing_person'])
        dict.__setitem__(self, key, value)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v

    def to_scrapy_item(self):
        item = ScrapyItem()
        for key, value in self.iteritems():
            item[key] = value
        return item