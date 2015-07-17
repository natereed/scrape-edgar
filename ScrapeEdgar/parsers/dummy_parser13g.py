import logging
import re

from ScrapeEdgar.parsers.html2textparser import HTML2TextParser

class DummyParser13g:
    def parse(self, doc, content_type='text/html'):
        #html_parser = HTML2TextParser()
        #self.html_parser.feed(doc)
        #text = html_parser.get_text()

        if content_type == 'text/html':
            return {'cusip': "90184L 102", 'address': "1355 Market Street, Suite 900, San Francisco, California 94103"}
        elif content_type == 'text/plain':
            return {'cusip': "90184L 102", 'address': "1355 Market Street, Suite 900, San Francisco, California 94103"}
        else:
            return {'cusip': "90184L 102", 'address': "1355 Market Street, Suite 900, San Francisco, California 94103"}

    def parse_text(self, text):

        return {'cusip': "90184L 102", 'address': "1355 Market Street, Suite 900, San Francisco, California 94103"}

    def parse_html(self, doc):
        logging.info("--------- parse html")

         # Convert to text
        html_parser = HTML2TextParser()
        html_parser.feed(doc)
        text = html_parser.get_text()

        return self.parse_text(text)

