from HTMLParser import HTMLParser

import logging
import re
from ScrapeEdgar.parsers.address_text_parser import parse_address
from ScrapeEdgar.parsers.html2textparser import HTML2TextParser

class Parser13ga:

    def parse(self, doc, content_type='text/html'):
        if content_type == 'text/html':
            return self.parse_html(doc)
        elif content_type == 'text/plain':
            return self.parse_text(doc)
        else:
            logging.warning("Unrecognized content type %s" % content_type)
            return None

    def parse_text(self, doc):
        cusip_pat = re.compile("(\w{6}\W*\w{3})\W+\(CUSIP Number\)", re.IGNORECASE | re.MULTILINE)

        #Alternative pattern
        # pat = re.compile("cusip (no|number|num)\.*:*\W*(\w{6}\W*\w{3})", re.IGNORECASE | re.MULTILINE)
        # TBD: Implement fallback to this pattern if the first one doesn't match (use match.group 2)

        cusip = None

        match = cusip_pat.search(doc)
        if match:
            cusip = match.group(1)

        address = parse_address(doc)

        return {'cusip' : cusip, 'address' : address}

    def parse_html(self, doc):
        # Convert to text
        html_parser = HTML2TextParser()
        html_parser.feed(doc)
        text = html_parser.get_text()

        return self.parse_text(text)
