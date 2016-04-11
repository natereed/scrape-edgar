import logging
import csv
import re
import os
import StringIO

import requests
import scrapy
from scrapy.http import FormRequest
from scrapy.spider import BaseSpider
from ScrapeEdgar.items import FilingItem
from ScrapeEdgar.cleaning_functions import clean_scraped_data
from ScrapeEdgar.parsers.parser13g import Parser13g
from ScrapeEdgar.parsers.parser13d import Parser13d
from ScrapeEdgar.parsers.parser13ga import Parser13ga
from ScrapeEdgar.parsers.parser8kEx101 import Parser8kEx101
from ScrapeEdgar.parsers.generic_parser import GenericParser

MULTI_VALUE_DELIMITTER = ';'
MAX_FIELD_LENGTH=100000

class EdgarSpider(BaseSpider):
    name = "edgar"
    allowed_domains = ["sec.gov","searchwww.sec.gov"]

    def __init__(self, input_file='companies.csv', search_key='name', **kwargs):
        self.input_file = input_file
        self.input_companies = kwargs.get('input_companies')
        self.search_key = search_key

    def load_companies(self):
        if self.input_companies:
            return self.input_companies.split(",")

        companies = []

        if re.match(r'https*', self.input_file):
            response = requests.request('GET', self.input_file)
            if response.status_code == 200:
                reader = csv.reader(StringIO.StringIO(response.content))
                for row in reader:
                    companies.append(row[0])
                return companies
            else:
                logging.error("Couldn't get companies from " + self.input_file)
                raise Exception("Unable to find companies to scrape. Aborting...")

        with open(self.input_file, "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                companies.append(row[0])
        return companies

    def load_ciks(self):
        logging.debug("Opening " + self.input_file)
        ciks = []

        if re.match(r'https*', self.input_file):
            logging.debug("Retrieving file from url")
            try:
                response = requests.request('GET', self.input_file)
                logging.debug("Got it!")
            except:
                logging.error("Unable to retrieve file from " + self.input_file)

            logging.debug("Reading file...")
            if response and response.status_code == 200:
                reader = csv.DictReader(StringIO.StringIO(response.content))
                for row in reader:
                    logging.debug(row)
                    ciks.append(row['CIK'])
                return ciks
            else:
                logging.error("Couldn't get companies from " + self.input_file)
                raise Exception("Unable to find companies to scrape. Aborting...")

        with open(self.input_file, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                ciks.append(row['CIK'])

        logging.debug("Loaded %d CIK's" % len(ciks))
        return ciks

    # The url's for scraping by CIK or company name, respectively:
    # CIK:          https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp?search_text=CUSIP&sort=Date&formType=1&isAdv=true&stemming=true&numResults=10&queryCik=1115222&numResults=10
    # Company name: https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp?search_text=CUSIP&sort=Date&formType=1&isAdv=true&stemming=true&numResults=10&queryCo=Dun%20and%20Bradstreet&numResults=10
    def start_requests(self):
        logging.debug("STARTING requests")
        form_requests = []
        formdata = {'search_text' : 'CUSIP',
                    'sort' : 'Date',
                    'formType' : '1',
                    'isAdv' : 'true',
                    'stemming' : 'true',
                    'numResults' : '10'}

        if self.search_key == 'cik':
            logging.debug("Searching by CIK's")
            ciks = self.load_ciks()
            for cik in ciks:
                logging.debug("CIK: " + cik)
                formdata.update({'queryCik' : cik})
                print str(formdata)
                form_requests.append(self.build_form_request(cik, formdata))
        else:
            logging.debug("Searching by company names")
            companies = self.load_companies()
            for company in companies:
                formdata.update({'queryCo' : company})
                form_requests.append(self.build_form_request(company, formdata))

        return form_requests

    def build_form_request(self, search_term, formdata):
        form_request = FormRequest("https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp",
                                   callback=self.parse_search_results_follow_next_page,
                                   formdata=formdata)
        form_request.meta['search_term'] = search_term
        form_request.meta['page_num'] = 1
        return form_request

    def parse_javascript_open(self, href):
        pat = re.compile("javascript:opennew\('([\w:\w/\.\-]+)'")
        m = re.search(pat, href)
        if m:
            return m.group(1)
        else:
            return None

    def select_parser(self, document_name, content_type):
        parser = None
        # TBD: Add 8k exhibits

        if re.match(u'SC 13G/A', document_name):
            parser = Parser13ga()
        #elif re.match(u'EX-4\.2 of 8-K', document_type): # Is this even used?
        #    parser = Parser8kEx42()
        elif re.match(u'SC 13G', document_name):
            parser = Parser13g()
        elif re.match(u'EX-1\.01 of 8-K',document_name):
            parser = Parser8kEx101()
        elif re.match(u'SC 13D', document_name):
            parser = Parser13d()
        else:
            logging.warn("Can't find parser for %s, %s. Using generic parser." % (document_name, content_type))
            parser = GenericParser()
        return parser

    def parse_document(self, response):
        logging.debug("------ parse_document ------")
        item = response.meta['item']
        #search_term = response.meta['search_term']
        search_term = item['search_term']

        logging.debug("search_term: " + search_term)

        document_name = item['document_name'].strip()
        logging.debug("document_name: " + document_name)
        logging.debug("--- Parse document %s" % document_name)

        content_type = response.headers['content-type']

        if response.status != 200:
            logging.error("Unable to retrieve %s " % document_name)
            yield item.to_scrapy_item()

        parser = self.select_parser(document_name, content_type)

        # Set item fields...
        if not parser:
            yield item.to_scrapy_item()

        logging.debug("PARSING %s with content type %s" % (document_name, content_type) )
        results = parser.parse(response.body, content_type=content_type)
        if results:
            clean_scraped_data(results, MULTI_VALUE_DELIMITTER, MAX_FIELD_LENGTH)
            logging.debug("--- Updating with results: ")
            logging.debug(results)
            item.update(results)
            logging.debug("--- Item:")
            logging.debug(item)
        else:
            logging.warning("No results from %s (%s) " % (item['url'], document_name))
        yield item.to_scrapy_item()

    def parse_search_results_follow_next_page(self, response):
        search_term = response.meta.get('search_term')
        page_num = response.meta.get('page_num')

        logging.debug("------ parse_search_results_follow_next_page -----")
        logging.debug("Page num: " + str(page_num))
        logging.debug("Search company: " + search_term)

        logging.info("Parsing search results for " + search_term + ", page " + str(page_num))
        logging.info("%d results" % len(response.xpath("//div[@id='ifrm2']/table[2]/tr")[1:]))

        for index, sel in enumerate(response.xpath("//div[@id='ifrm2']/table[2]/tr")[1:]):
            logging.debug("Index: " + str(index))
            date = sel.xpath("td[1]/i/text()").extract()
            if len(date) == 0:
                continue
            else:
                date = date[0]

            href = sel.xpath("td/a[@id='viewFiling']/@href").extract()
            logging.debug("HREF: " + str(href))
            if len(href) == 0:
                continue
            else:
                href = href[0]

            url = self.parse_javascript_open(href)
            document_name = sel.xpath("td[2]/a/text()").extract()[0].strip()
            filing_item = FilingItem()
            # Scrape issuer name
            filing_item['document_name'] = document_name
            filing_item['date'] = date
            filing_item['url'] = url
            filing_item['search_term'] = search_term
            request = scrapy.Request(url, callback=self.parse_document)
            request.meta['item'] = filing_item
            request.meta['search_term'] = search_term # Set this for the next page of search results
            logging.debug("Setting search company " + search_term + " for document_name " + document_name)
            if not request.meta['search_term']:
                logging.error("No search company set in request.meta!")

            yield request

        # Follow next
        next_page = response.xpath("//table[@id='header']//a[@title='Next Page']/@href")

        if next_page:
            logging.debug("Following next page...")
            url = response.urljoin(next_page[0].extract())
            request = scrapy.Request(url, self.parse_search_results_follow_next_page)
            request.meta['search_term'] = search_term # Set this for the next page of search results
            request.meta['page_num'] = page_num + 1
            yield request

