import logging
import re

from ScrapeEdgar.parsers.html2textparser import HTML2TextParser
from ScrapeEdgar.parsers.address_text_parser import parse_address

class Parser13g:
    def parse(self, doc, content_type='text/html'):
        if content_type == 'text/html':
            return self.parse_html(doc)
        elif content_type == 'text/plain':
            return self.parse_text(doc)
        else:
            logging.warning("Unrecognized content type %s" % content_type)
            return None

    def parse_text(self, text):
        cusip_number = None
        address = None

        pat = re.compile(r'cusip (no|number|num|#)\.*:*\W*(\w{6}\W*\w{3})\b', re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            cusip_number = match.group(2).strip()
        else:
            pat = re.compile(r'cusip\s+number\s+(\w{6}\W*\w{3})\b', re.IGNORECASE | re.MULTILINE)
            match = pat.search(text)
            if match:
                cusip_number = match.group(1).strip()
            else:
                logging.warning("No match for cusip #")

        address = parse_address(text)

        return {'cusip': cusip_number, 'address': address}

    def parse_html(self, doc):
         # Convert to text
        html_parser = HTML2TextParser()
        html_parser.feed(doc)
        text = html_parser.get_text()

        return self.parse_text(text)

