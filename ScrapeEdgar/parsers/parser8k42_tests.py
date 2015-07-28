import unittest

from ScrapeEdgar.parsers.parser8k42 import Parser8kEx42
from test_utils import load_file_contents

# See: http://www.sec.gov/Archives/edgar/data/1115222/000119312512489386/d448291dex42.htm
class Parser8k42Tests():
    def setUp(self):
        self.parser = Parser8kEx42()

    def test_parser8kex42(self):
        contents = load_file_contents("example_filings/EX-4.2-DNB.html")
        parser = Parser8kEx42()
        results = parser.parse(contents)
        self.assertEqual(['26483E AH3'], results.get('cusip'))
        self.assertEqual("4.000% Senior Notes due 2020", results.get("description"))
        self.assertEqual(u'THE DUN\xa0& BRADSTREET CORPORATION', results.get("issuer_name"))

