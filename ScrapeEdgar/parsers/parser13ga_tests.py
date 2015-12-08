import unittest

from ScrapeEdgar.parsers.parser13ga import Parser13ga
from ScrapeEdgar.parsers.test_utils import load_file_contents

class Parser13gaTests(unittest.TestCase):
    def setUp(self):
        self.parser = Parser13ga()

    #@unittest.skip("testing skipping")
    def test_parser13ga(self):
        contents = load_file_contents("example_filings/twitter13ga.html")
        results = self.parser.parse(contents)
        print results

        self.assertEqual("90184L 102", results.get('cusip'))
        self.assertEqual("1355 Market Street, Suite 900, San Francisco, California 94103", results.get('address'))
        self.assertEqual("Twitter, Inc.", results.get('issuer_name'))
        self.assertEqual('Common Stock, par value $0.000005 per share', results.get('issue_name'))

    #@unittest.skip("testing skipping")
    def test_parse13ga_txt(self):
        contents = load_file_contents("example_filings/albemarle_13ga.txt")
        results = self.parser.parse(contents, 'text/plain')
        self.assertEqual("012653101", results.get('cusip'))
        self.assertEqual("451 Florida Street, Baton Rouge, LA 70801", results.get('address'))
        self.assertEqual("Albemarle Corporation", results.get("issuer_name"))
        self.assertEqual("Common Stock", results.get("issue_name"))

    #@unittest.skip("testing skipping")
    def test_parse13ga_txt_dnb_none_type_for_address(self):
        contents = load_file_contents("example_filings/13ga-dun.bradstreet.corp.txt")
        results = self.parser.parse(contents, 'text/plain')
        self.assertEqual("26483E100", results.get('cusip'))
        self.assertEqual("103 JFK PARKWAY SHORT HILLS NJ 07078", results.get('address'))
        self.assertEqual("DUN & BRADSTREET CORP", results.get("issuer_name"))
        self.assertEqual("Common Stock", results.get("issue_name"))

    #@unittest.skip("testing skipping")
    def test_parse13ga_html_missing_address(self):
        contents = load_file_contents("example_filings/twitter_sc13ga_did_not_parse_address.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("90184L102", results.get('cusip'))
        self.assertEqual("Twitter, Inc.", results.get("issuer_name"))
        self.assertEqual("Common Stock, $0.000005 par value\nper share", results.get("issue_name"))
        # TBD: Fix this
        self.assertEqual("1355 Market Street, Suite 900, San Francisco, CA 94103", results.get('address'))

    def test_missing_cusip_number_for_dnb_13ga(self):
        # The title says "13G," but below there is text that says "Ammendment #1 and this comes back in the
        # search results as a 13G/A:
        # http://www.sec.gov/Archives/edgar/data/1115222/000114036115006261/doc1.htm

        contents = load_file_contents("example_filings/dnb13ga_missing_cusip.html")
        results = self.parser.parse(contents, content_type="text/html")
        print "---- %s  ------ " % str(results)
        self.assertEqual("26483E100", results.get('cusip'))
        self.assertEqual("COMMON STOCK", results.get("issue_name"))
        self.assertEqual("DUN   BRADSTREET CORP", results.get("issuer_name"))
        self.assertEqual("103 JFK PARKWAY, SHORT HILLS, NJ 07078", results.get("address"))

    #@unittest.skip("testing skipping")
    def test_missing_cusip_number_for_dnb_13ga_filing_txt(self):
        contents = load_file_contents("example_filings/dnb_13ga_filing.txt")
        results = self.parser.parse(contents, content_type="text/plain")
        # See: http://www.sec.gov/Archives/edgar/data/1115222/000031506615001878/filing.txt
        self.assertEqual("DUN & BRADSTREET CORP DEL NEW", results.get("issuer_name"))
        self.assertEqual("103 JFK PKWY, SHORT HILLS, NJ 07078, USA", results.get("address"))
        self.assertEqual("COMMON STOCK", results.get("issue_name"))
        self.assertEqual("26483E100", results.get('cusip'))

    #@unittest.skip("testing skipping")
    def test_extract_issue_name_from_13ga(self):
        #Example: http://www.sec.gov/Archives/edgar/data/1115222/000021545715000168/dun.bradstreet.corp.txt
        # appears under "Title of Class of Securities"
        # TBD
        # DNB
        contents = load_file_contents("example_filings/dnb13ga.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("COMMON STOCK", results.get('issue_name'))

        # Twitter
        contents = load_file_contents("example_filings/twitter13ga.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("Common Stock, par value $0.000005 per share", results.get("issue_name"))

    #@unittest.skip("testing skipping")
    def test_extract_issue_name_from_13ga_text(self):
        contents = load_file_contents("example_filings/13ga-dun.bradstreet.corp.txt")
        results = self.parser.parse(contents, content_type="text/plain")
        print results
        self.assertEqual("Common Stock", results.get('issue_name'))

    #@unittest.skip("testing skipping")
    def test_extract_issuer_name_from_13ga_text(self):
        contents = load_file_contents("example_filings/13ga-dun.bradstreet.corp.txt")
        results = self.parser.parse(contents, content_type="text/plain")
        print results
        self.assertEqual("DUN & BRADSTREET CORP", results.get("issuer_name"))

    #@unittest.skip("testing skipping")
    def test_extract_fields_from_nike_13ga_alt_format(self):
        contents = load_file_contents("example_filings/nike_13ga_alt_format.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("Common Stock", results.get("issue_name"))
        self.assertEqual("NIKE\nInc", results.get("issuer_name"))
        self.assertEqual("654106103", results.get("cusip"))

if __name__ == '__main__':
    unittest.main()
