from ScrapeEdgar.parsers.base_parser import BaseParser

import re

class Parser8kEx402(BaseParser):

    # Company name can be in various formats, eg.
    #   Company, Inc
    #   Company, Inc.
    #   COMPANY INC
    #   COMPANY LLC, COMPANY L.L.C.
    #   etc
    # This method returns a regex that will match any of those variations of company name
    def standardize_company_regex(self, issuer_name):
        issuer_name = re.sub(r',*\s+INC\.*$', r',*\s+INC\.*', issuer_name, flags=re.IGNORECASE)
        issuer_name = re.sub(r',*\s+L\.*L\.*C\.*$', r',*\s+L\.*L\.*C\.*', issuer_name, flags=re.IGNORECASE)
        return issuer_name

    def normalize(self, issue_name):
        return re.sub('\s+', ' ', issue_name)

    def parse_text(self, text, **kwargs):
        exp = self.standardize_company_regex(kwargs['issuer_name']) + r'\s+([\w\W]+?)PRINCIPAL AMOUNT'

        pat = re.compile(exp, re.IGNORECASE | re.MULTILINE)

        match = pat.search(text)
        issue_name = None
        if match:
            issue_name = self.normalize(match.group(1)).strip()
            print "Issue name: %s" % issue_name

        cusip = None
        pat = re.compile(r'CUSIP:*\W*(\w{6}\W*\w{3})\b', re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            cusip = match.group(1)

        return {'issue_name' : issue_name, 'cusip' : cusip}






