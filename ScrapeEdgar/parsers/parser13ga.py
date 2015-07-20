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
        patterns_to_match_groups = {
            r'(\w{6}\W*\w{3})\W+\(CUSIP Number\)': 1,
            r'cusip (no|number|num)\.*:*\W*(\w{6}\W*\w{3})' : 2
        }

        cusip = None
        for pat in patterns_to_match_groups:
            match = re.compile(pat, re.IGNORECASE | re.MULTILINE).search(doc)
            if match:
                cusip = match.group(patterns_to_match_groups.get(pat))
                break

        address = parse_address(doc)

        issue_name = None
        pat = re.compile(r"\(Name\s+of\s+Issuer\)([a-z0-9\.%'\s\,\$]+)-*\s+\(Title\s+of\s+Class\s+of\s+Securities\)", re.IGNORECASE | re.MULTILINE)
        match = pat.search(doc)
        if match:
            issue_name = match.group(1).strip()

        return {'cusip' : cusip, 'address' : address, 'issue_name' : issue_name}

    def parse_html(self, doc):
        # Convert to text
        html_parser = HTML2TextParser()
        html_parser.feed(doc)
        text = html_parser.get_text()

        return self.parse_text(text)
