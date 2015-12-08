from ScrapeEdgar.parsers.address_text_parser import parse_address
from ScrapeEdgar.parsers.base_parser import BaseParser

import logging
import re

class Parser13ga(BaseParser):
    def parse_text(self, doc, **kwargs):
        with open("tmp.html", "w") as out_file:
            out_file.write(doc)

        # CUSIP
        cusip = None
        pat = r'(\w{6}\W*\w{3})\W+\(CUSIP Number\)'
        match = re.compile(pat, re.IGNORECASE | re.MULTILINE).search(doc)
        if match:
            cusip = match.group(1)
        else:
            pat = r'cusip (no|number|num)\.*:*\W*(\w{6}\W*\w{3})'
            match = re.compile(pat, re.IGNORECASE | re.MULTILINE).search(doc)
            if match:
                cusip = match.group(2)
            else:
                logging.warning("No match for cusip")

        # Address
        address = parse_address(doc)

        # Issue
        issue_name = None
        pat = re.compile(r"\(Name\s+of\s+Issuer\)([\w\W]+?)-*\s+\(Title\s+of\s+Class\s+of\s+Securities\)", re.IGNORECASE | re.MULTILINE)
        match = pat.search(doc)
        if match:
            issue_name = match.group(1).strip()
        else:
            pat = re.compile(r'Title\s+of\s+Class\s+of\s+Securities:\s+([\w\W]+?)\s+(Item 2\(e\)\.*)?\s+CUSIP\s+Number:', re.IGNORECASE | re.MULTILINE)
            match = pat.search(doc)
            if match:
                issue_name = match.group(1).strip()
            else:
                logging.warning("No match for issue name")

        # Issuer
        issuer_name = None
        pat = re.compile(r"\(Amendment\s+No\.*:*\s+[\w\W]*?\)\*?\s+(Under\s+the\s+Securities\s+Exchange\s+Act\s+of\s+1934)?([\w\W]+?)-*\(Name\s+of\s+Issuer\)", re.IGNORECASE | re.MULTILINE)
        match = pat.search(doc)
        if match:
            issuer_name = match.group(2).strip()
            match = re.match(r'(.*?)\s*-+$', issuer_name)
            if match:
                issuer_name = match.group(1).strip()
        else:
            pat = re.compile(r'Item\s+1\(a\)\.*\s*-*\s*Name\s+of\s+Issuer:([\w\W]+?)Item', re.IGNORECASE | re.MULTILINE)
            match = pat.search(doc)
            if match:
                issuer_name = match.group(1).strip()
            else:
                logging.warning("No match for issuer name in SC13G/A")

        return {'cusip' : cusip, 'address' : address, 'issue_name' : issue_name, 'issuer_name' : issuer_name}

