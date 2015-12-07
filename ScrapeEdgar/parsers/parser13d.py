import re
import logging

from ScrapeEdgar.parsers.base_parser import BaseParser
from ScrapeEdgar.parsers.address_text_parser import parse_address

class Parser13d(BaseParser):
    def parse_text(self, text, **kwargs):
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

        issuer_name = None
        pat = re.compile(r"\(Amendment\s+No\.\s+[0-9]?\)\*?\s+([\w\W]+)\(Name\s+of\s+Issuer\)", re.IGNORECASE | re.MULTILINE)
        f = open("text.txt", "w")
        f.write(text)
        f.close()

        match = pat.search(text)
        print "--- match"
        print match

        if match:
            print "Match!"
            issuer_name = match.group(1).strip()

        print "issuer name: %s" % issuer_name
        return {'cusip': [cusip_number], 'address': address, 'parsed_issuer_name' : issuer_name}
