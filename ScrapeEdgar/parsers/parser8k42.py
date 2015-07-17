import lxml.html
import re

from lxml.cssselect import CSSSelector

from ScrapeEdgar.parsers.html2textparser import HTML2TextParser

class Parser8kEx42:
    def parse(self, doc, content_type='text/html'):
        if content_type == 'text/html':
            return self.parse_html(doc)
        elif content_type == 'text/plain':
            return self.parse_text(doc)
        else:
            print "--- Warning! Unrecognized content type %s" % content_type
            return None

    def parse_text(self, doc):
        print "WARNING: TEXT PARSER for EX4.2 not implemented!!!"
        return

    def parse_html(self, doc):
        # build the DOM Tree
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
