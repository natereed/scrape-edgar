import logging
from ScrapeEdgar.parsers.html2textparser import HTML2TextParser

class BaseParser:
    def parse(self, doc, content_type='text/html', **kwargs):
        results = None
        if content_type == 'text/html':
            results = self.parse_html(doc, **kwargs)
        elif content_type == 'text/plain':
            results = self.parse_text(doc, **kwargs)
        else:
            logging.warning("Unrecognized content type %s" % content_type)
            return None

        results['issuer_name'] = kwargs.get('issuer_name')
        results['search_company'] = kwargs.get('search_company')
        return results

    def parse_html(self, doc, **kwargs):
         # Convert to text
        html_parser = HTML2TextParser()
        html_parser.feed(doc)
        text = html_parser.get_text()

        return self.parse_text(text, **kwargs)
    def parse_text(self, text, **kwargs):
        print "Not implemented!!!"
        return {}


