import re
import logging

from ScrapeEdgar.parsers.base_parser import BaseParser
from ScrapeEdgar.parsers.address_text_parser import parse_address

class Parser13d(BaseParser):
    def parse_text(self, text, **kwargs):
        print text

        print "OK!!!!!"
        cusip_number = None
        address = None

        pat = re.compile(r'(\w{6}\W*\w{3})\s+\(cusip\s+(no|number|num|#)\)', re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            print "MATCHES!!!!"
            cusip_number = match.group(1).strip()
            print cusip_number
        else:
            print "NO MATCH!"
            logging.warning("No match for cusip #")

        address = parse_address(text)

        issue_name = None
        pat = re.compile(r"\(Name\s+of\s+Issuer\)([a-z0-9\.%'\s\,\$]+)-*\s+\(Title\s+of\s+Class\s+of\s+Securities\)", re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            issue_name = match.group(1).strip()

        else:
            pat = re.compile(r'Item 2\(d\)\.\s+Title\s+of\s+Class\s+of\s+Securities:\s+([\w\W]+)\s+Item\s+2\(e\)')
            match = pat.search(text)
            if match:
                issue_name = match.group(1).strip()

        return {'cusip': cusip_number, 'address': address, 'issue_name' : issue_name}
