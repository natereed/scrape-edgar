from ScrapeEdgar.parsers.base_parser import BaseParser

import re

class Parser8kEx101(BaseParser):
   def parse_text(self, text, **kwargs):
      pat = re.compile(r'principal amount of ([\w\W]+?) to be issued', re.IGNORECASE | re.MULTILINE)

      match = pat.search(text)

      issue_name = None
      if match:
         issue_name = match.group(1)

      cusip = None
      pat = re.compile(r'CUSIP/ISIN:\s+(\w{6}\W*\w{3})', re.IGNORECASE | re.MULTILINE)
      match = pat.search(text)
      if match:
         cusip = match.group(1)

      return {'issue_name' : issue_name, 'cusip' : cusip}
