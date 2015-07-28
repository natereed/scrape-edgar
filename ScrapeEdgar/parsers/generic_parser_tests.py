import unittest

from ScrapeEdgar.parsers.generic_parser import GenericParser
from ScrapeEdgar.parsers.test_utils import load_file_contents

# See: http://www.sec.gov/Archives/edgar/data/936468/000119312508053896/dex42.htm
#      more

class GenericParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = GenericParser()

    def test_extract_from_ex42(self):
        contents = load_file_contents("example_filings/EX-4.2-Lockheed.html")
        results = self.parser.parse(contents)
        self.assertEqual(['539830 AS8'], results.get("cusip"))
        self.assertEqual(['4.121% NOTE DUE 2013'], results.get("issue_name"))

    def test_extract_multiple_cusips(self):
        contents = load_file_contents("example_filings/EX-99-multiple_convertible_notes.html")
        results = self.parser.parse(contents)
        self.assertEqual(['229678AD9', '229678AH0', '229678AF4'], results.get("cusip"))

    def test_extract_multiple_issues(self):
        contents = load_file_contents("example_filings/EX-99-multiple_convertible_notes.html")
        results = self.parser.parse(contents)
        self.assertEqual(['1.125% CONVERTIBLE SENIOR NOTES DUE 2018',
                          '1.875% CONVERTIBLE SENIOR NOTES DUE 2020',
                          '2.50% CONVERTIBLE SENIOR NOTES DUE 2017'], results.get("issue_name"))

    def test_extract_from_other_ex42(self):
        contents = load_file_contents("example_filings/EX-4.2-DNB.html")
        results = self.parser.parse(contents)
        self.assertEqual(['26483E AH3'], results.get("cusip"))
        self.assertEqual(['4.000% SENIOR NOTES DUE 2020'], results.get("issue_name"))

    def test_broken_issuer_name_sc13d(self):
        contents = load_file_contents("example_filings/sc13d_broken_issuer_name.html")
        results = self.parser.parse(contents)
        self.assertEqual(['63888U108'], results.get('cusip'))
        self.assertEqual('Common Stock, $0.001 Par Value per share', results.get('issue_name'))