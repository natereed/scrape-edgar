import logging
import re

from ScrapeEdgar.parsers.base_parser import BaseParser
from ScrapeEdgar.parsers.address_text_parser import parse_address

class Parser13g(BaseParser):

    def parse_text(self, text, **kwargs):
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

        # Issuer
        issuer_name = None
        pat = re.compile(r"\(Amendment\s+No\.*:*\s+[\w\W]*?\)\*?\s+(Under\s+the\s+Securities\s+Exchange\s+Act\s+of\s+1934)?([\w\W]+?)-*\(Name\s+of\s+Issuer\)", re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            issuer_name = match.group(2).strip()
            match = re.match(r'(.*?)\s*-+$', issuer_name)
            if match:
                issuer_name = match.group(1).strip()
        else:
            pat = re.compile(r'Item\s+1\(a\)\.*\s*-*\s*Name\s+of\s+Issuer:([\w\W]+?)Item', re.IGNORECASE | re.MULTILINE)
            match = pat.search(text)
            if match:
                issuer_name = match.group(1).strip()
            else:
                logging.warning("No match for issuer name in SC13G/A")

        return {'cusip': cusip_number, 'address': address, 'issue_name' : issue_name, 'issuer_name' : issuer_name}



