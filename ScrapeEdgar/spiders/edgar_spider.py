import logging
import csv
import os
import re
import types
from urlparse import urlparse
from posixpath import basename
import StringIO

import requests
import scrapy
from scrapy.http import FormRequest
from scrapy.spider import BaseSpider
from ScrapeEdgar.items import FilingItem
from ScrapeEdgar.cleaning_functions import clean_scraped_data
from ScrapeEdgar.parsers.parser13g import Parser13g
from ScrapeEdgar.parsers.parser13ga import Parser13ga
from ScrapeEdgar.parsers.parser8kEx101 import Parser8kEx101
from ScrapeEdgar.parsers.parser8kEx402 import Parser8kEx402
from ScrapeEdgar.parsers.generic_parser import GenericParser

MULTI_VALUE_DELIMITTER = ';'
MAX_FIELD_LENGTH=100000

class EdgarSpider(BaseSpider):
    name = "edgar"
    allowed_domains = ["sec.gov","searchwww.sec.gov"]

    def __init__(self, input_file='companies.csv', **kwargs):
        self.input_file = input_file

    def extract_issuer_name(self, document_name):
        logging.info("Extracting issuer name from " + document_name)
        pat = re.compile(r'for ([\w\W]+)$')
        match = pat.search(document_name)
        if match:
            logging.info("ISSUER NAME match: %s" % match.group(1))
            return match.group(1)
        else:
            logging.info("No match for issuer name")

    def load_companies(self):
        companies = []

        if re.match(r'https*', self.input_file):
            response = requests.request('GET', self.input_file)
            if response.status_code == 200:
                reader = csv.DictReader(StringIO.StringIO(response.content))
                for row in reader:
                    companies.append(row['COMPANY'])
                return companies
            else:
                logging.error("Couldn't get companies from " + self.input_file)
                raise Exception("Unable to find companies to scrape. Aborting...")

        with open(self.input_file, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                companies.append(row['COMPANY'])
        return companies

    #https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp?search_text=CUSIP&sort=Date&formType=1&isAdv=true&stemming=true&numResults=10&queryCo=Dun%20and%20Bradstreet&numResults=10
    def start_requests(self):
        #companies = ['Twitter', 'Dun and Bradstreet', 'Google']
        companies = self.load_companies()
        form_requests = []
        for company in companies:
            form_request = FormRequest("https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp",
                                       formdata = {'search_text' : 'CUSIP',
                                                   'sort' : 'Date',
                                                   'formType' : '1',
                                                   'isAdv' : 'true',
                                                   'stemming' : 'true',
                                                   'numResults' : '10',
                                                   'queryCo' : company},
                                       callback=self.parse_search_results_follow_next_page)
            form_request.meta['search_company'] = company
            form_requests.append(form_request)

        return form_requests

    def parse_javascript_open(self, href):
        pat = re.compile("javascript:opennew\('([\w:\w/\.\-]+)'")
        m = re.search(pat, href)
        if m:
            return m.group(1)
        else:
            return None

    def select_parser(self, document_type, content_type):
        parser = None
        # TBD: Add 8k exhibits

        if re.match(u'SC 13G/A', document_type):
            parser = Parser13ga()
        #elif re.match(u'EX-4\.2 of 8-K', document_type): # Is this even used?
        #    parser = Parser8kEx42()
        elif re.match(u'SC 13G', document_type):
            parser = Parser13g()
        elif re.match(u'EX-1\.01 of 8-K',document_type):
            parser = Parser8kEx101()
        else:
            logging.warn("Can't find parser for %s, %s. Using generic parser." % (document_type, content_type))
            parser = GenericParser()
        return parser

    def parse_document(self, response):
        item = response.meta['item']
        response = requests.get(item['url'])
        document_name = item['document_name'].strip()
        logging.info("--- Parse document %s, %s: " % (document_name, item['issuer_name']))

        content_type = response.headers['content-type']

        if response.status_code != 200:
            logging.error("Unable to retrieve %s " % document_name)
            return item

        # Save response to downloads
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        parsed_url = urlparse(item['url'])
        out = open("downloads/%s" % basename(parsed_url.path), "w")
        out.write(response.text)
        out.close()

        parser = self.select_parser(document_name, content_type)

        # Set item fields...
        if not parser:
            return item

        logging.info("PARSING %s with content type %s" % (document_name, content_type) )
        logging.info("ISSUER: %s" % item['issuer_name'])
        results = parser.parse(response.text, content_type=content_type, issuer_name=item['issuer_name'])
        if results:
            clean_scraped_data(results, MULTI_VALUE_DELIMITTER, MAX_FIELD_LENGTH)
            print "--- Updating with results: "
            print results
            item.update(results)
        else:
            logging.warning("No results from %s (%s) " % (item['url'], document_name))
        return item

    def parse_search_results_follow_next_page(self, response):
        search_company = response.meta.get('search_company')

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
            document_name = sel.xpath("td[2]/a/text()").extract()[0].strip()
            filing_item = FilingItem()
            # Scrape issuer name
            filing_item['issuer_name'] = search_company
            filing_item['document_name'] = document_name
            filing_item['date'] = date
            filing_item['url'] = url
            request = scrapy.Request(url, callback=self.parse_document)
            request.meta['item'] = filing_item
            request.meta['search_company'] = search_company # Set this for the next page of search results
            if not request.meta['search_company']:
                logging.error("No search company set in request.meta!")

            yield request

        # Follow next
        next_page = response.xpath("//table[@id='header']//a[@title='Next Page']/@href")

        if next_page:
            url = response.urljoin(next_page[0].extract())
            request = scrapy.Request(url, self.parse_search_results_follow_next_page)
            request.meta['search_company'] = search_company # Set this for the next page of search results
            yield request

