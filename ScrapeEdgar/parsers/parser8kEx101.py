from ScrapeEdgar.parsers.base_parser import BaseParser

import re

class Parser8kEx101(BaseParser):
   def parse_text(self, text, *args):
      pat = re.compile(r'principal amount of ([\w\W]+?) to be issued', re.IGNORECASE | re.MULTILINE)

      print text
      f = open("tmp_8kex101.txt", "w")
      f.write(text)
      f.close()

      match = pat.search(text)

      issue_name = None
      if match:
         issue_name = match.group(1)

      return {'issue_name' : issue_name}
