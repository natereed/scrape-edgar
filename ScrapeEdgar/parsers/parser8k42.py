import lxml.html
import re

from lxml.cssselect import CSSSelector

from ScrapeEdgar.parsers.html2textparser import HTML2TextParser
from ScrapeEdgar.parsers.base_parser import BaseParser

class Parser8kEx42(BaseParser):
   
    def parse_text(self, doc, **kwargs):
        print "WARNING: TEXT PARSER for EX4.2 not implemented!!!"
        return

    def parse_html(self, doc, **kwargs):
        # build the DOM Tree
        # TBD: Rewrite this to use text parsing
        tree = lxml.html.fromstring(doc)

        # construct a CSS Selector
        sel = CSSSelector('hr + p')

        # Apply the selector to the DOM tree.
        name = sel(tree)[0].text.strip()

        # Convert to text
        html_parser = HTML2TextParser()
        html_parser.feed(doc)
        text = html_parser.get_text()

        # CUSIP
        pat = re.compile("cusip (no|number|num)\.*:*\W*(\w{6}\W*\w{3})", re.IGNORECASE)
        m = pat.finditer(text)
        cusips = [match.group(2) for match in m]

        sel = CSSSelector("hr + p + p")
        description = sel(tree)[0].text.strip()

        return {'issuer_name': name, "description" : description, "cusip" : list(set(cusips))}
