import logging
from ScrapeEdgar.parsers.html2textparser import HTML2TextParser

class BaseParser:
    def parse(self, doc, content_type='text/html', *args):
        if content_type == 'text/html':
            return self.parse_html(doc, *args)
        elif content_type == 'text/plain':
            return self.parse_text(doc, *args)
        else:
            logging.warning("Unrecognized content type %s" % content_type)
            return None

    def parse_html(self, doc, *args):
         # Convert to text
        html_parser = HTML2TextParser()
        html_parser.feed(doc)
        text = html_parser.get_text()

        return self.parse_text(text, *args)

    def parse_text(self, text, *args):
        print "Not implemented!!!"
        return {}


