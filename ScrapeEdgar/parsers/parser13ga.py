from ScrapeEdgar.parsers.base_parser import BaseParser
import re
from ScrapeEdgar.parsers.address_text_parser import parse_address

class Parser13ga(BaseParser):
    def parse_text(self, doc, **kwargs):
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

