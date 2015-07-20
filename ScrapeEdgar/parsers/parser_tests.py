import unittest
from ScrapeEdgar.parsers.parser13g import Parser13g
from ScrapeEdgar.parsers.parser8k42 import Parser8kEx42
from ScrapeEdgar.parsers.test_utils import load_file_contents

class ParserTests(unittest.TestCase):

    def setUp(self):
        self.parser = Parser13g()

    def test_parser8kex42(self):
        contents = load_file_contents("example_filings/EX-4.2-DNB.html")
        parser = Parser8kEx42()
        results = parser.parse(contents)
        self.assertEqual(['26483E AH3'], results.get('cusip'))
        self.assertEqual("4.000% Senior Notes due 2020", results.get("description"))
        self.assertEqual(u'THE DUN\xa0& BRADSTREET CORPORATION', results.get("issuer_name"))

    def test_parse13g_html(self):
        contents = load_file_contents("example_filings/SC_13G_Twitter.html")
        results = self.parser.parse(contents, content_type="text/html")
        results = {'cusip' : '90184L 102', 'address' : '1355 Market Street, Suite 900, San Francisco, California 94103'}
        self.assertEqual("90184L 102", results.get('cusip'))
        self.assertEqual("1355 Market Street, Suite 900, San Francisco, California 94103", results.get('address'))

    def test_sc13g_mismatched_address(self):
        contents = load_file_contents("example_filings/sc13g_doc1_dnb_mismatched_address.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("26483E100", results.get('cusip'))
        self.assertEqual("103 JFK PARKWAY, SHORT HILLS, NJ 07078", results.get('address'))

    # This is caused by the comma appearing after 2., eg:
    #Item 2., (a), Name of Person Filing:
    def test_sc13g_2a_comma_breakage(self):
        contents = load_file_contents("example_filings/sc13g_comma_breakage.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("26483E100", results.get('cusip'))
        self.assertEqual("103 JFK PARKWAY, SHORT HILLS, NJ 07078", results.get('address'))

    def test_sc13_twitter_cusip_parsed_incorrectly(self):
        contents = load_file_contents("example_filings/sc13g_twitter_cusip_parsed_incorrectly.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("90184L102", results.get('cusip'))
        self.assertEqual("1355 Market Street, Suite 900, San Francisco, California 94103", results.get('address'))

    # TBD (need to find an actual text document for this):
    #def test_parse13_text(self):

    def extract_issue_name_from_13g(self):
        pass

    def test_extract_cusip_number_from_fwp(self):
        # http://www.sec.gov/Archives/edgar/data/1115222/000119312515216527/d939676dfwp.htm
        print "Not yet implemented"
        pass

    def test_extract_cusip_from_ex1_8k(self):
        #http://www.sec.gov/Archives/edgar/data/1115222/000119312515220904/d941511dex11.htm
        print "Not yet implemented"

    def test_extract_issue_name_from_ex1_8k(self):
        #http://www.sec.gov/Archives/edgar/data/1115222/000119312515220904/d941511dex11.htm
        pass

if __name__ == '__main__':
    unittest.main()

