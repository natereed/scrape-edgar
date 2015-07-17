import logging

import os
import re
import requests
import scrapy
from urlparse import urlparse
from posixpath import basename
from scrapy.http import FormRequest
from scrapy.spider import BaseSpider
from ScrapeEdgar.items import FilingItem
from ScrapeEdgar.parsers.parser13g import Parser13g
from ScrapeEdgar.parsers.parser13ga import Parser13ga
from ScrapeEdgar.parsers.parser8k42 import Parser8kEx42

class EdgarSpider(BaseSpider):
    name = "edgar"
    allowed_domains = ["sec.gov","searchwww.sec.gov"]

    def read_companies(self):
        f = open("cusip-daily-issuer.csv", "r")

    #https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp?search_text=CUSIP&sort=Date&formType=1&isAdv=true&stemming=true&numResults=10&queryCo=Dun%20and%20Bradstreet&numResults=10
    def start_requests(self):
        companies = ['Twitter', 'Dun and Bradstreet']
        return [FormRequest("https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp",
                           formdata = {'search_text' : 'CUSIP',
                            'sort' : 'Date',
                            'formType' : '1',
                            'isAdv' : 'true',
                            'stemming' : 'true',
                            'numResults' : '10',
                            'queryCo' : company},
                           callback=self.parse_search_results_follow_next_page)
                for company in companies]

    def parse_javascript_open(self, href):
        pat = re.compile("javascript:opennew\('([\w:\w/\.\-]+)'")
        m = re.search(pat, href)
        if m:
            return m.group(1)
        else:
            return None

    def select_parser(self, document_type, content_type):
        parser = None
        if re.match(u'SC 13G/A', document_type):
            parser = Parser13ga()
        elif re.match(u'EX-4.2 of 8-K', document_type):
            parser = Parser8kEx42()
        elif re.match(u'SC 13G', document_type):
            parser = Parser13g()
        else:
            logging.warn("Can't find parser for %s, %s" % (document_type, content_type))
        return parser

    def parse_document(self, response):
        item = response.meta['item']
        response = requests.get(item['url'])
        name = item['name'].strip()
        content_type = response.headers['content-type']

        if response.status_code != 200:
            logging.error("Unable to retrieve %s " % name)
            return item

        # Save response to downloads
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        parsed_url = urlparse(item['url'])
        out = open("downloads/%s" % basename(parsed_url.path), "w")
        out.write(response.text)
        out.close()

        parser = self.select_parser(name, content_type)

        # Set item fields...
        if not parser:
            return item

        logging.info("PARSING %s with content type %s" % (name, content_type) )
        results = parser.parse(response.text, content_type)
        print "------- Address for %s, %s, %s " % (item['url'], name, results['address'][:100])

        if results:
            item.update(results)
        else:
            logging.warning("No results from %s (%s) " % (item['url'], name))
        return item

    def parse_search_results_follow_next_page(self, response):
        for index, sel in enumerate(response.xpath("//div[@id='ifrm2']/table[2]/tr")[1:]):
            date = sel.xpath("td[1]/i/text()").extract()
            if len(date) == 0:
                continue
            else:
                date = date[0]

            href = sel.xpath("td/a[@id='viewFiling']/@href").extract()
            if len(href) == 0:
                continue
            else:
                href = href[0]

            url = self.parse_javascript_open(href)
            name = sel.xpath("td[2]/a/text()").extract()[0]
            filing_item = FilingItem()
            filing_item['name'] = name
            filing_item['date'] = date
            filing_item['url'] = url
            request = scrapy.Request(url, callback=self.parse_document)
            request.meta['item'] = filing_item
            yield request

        # Follow next
        next_page = response.xpath("//table[@id='header']//a[@title='Next Page']/@href")

        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_search_results_follow_next_page)

