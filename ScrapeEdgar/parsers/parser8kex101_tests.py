import re
import unittest

from ScrapeEdgar.parsers.parser8kEx101 import Parser8kEx101
from ScrapeEdgar.parsers.test_utils import load_file_contents

# Tests for term sheet (8K ex 1.01)
# See: http://www.sec.gov/Archives/edgar/data/1288776/000119312514066560/d681994dex101.htm

class Parser8kEx101Tests(unittest.TestCase):
    def setUp(self):
        self.parser = Parser8kEx101()
        contents = load_file_contents("example_filings/google-EX-1.01-term-sheet.html")
        self.results = self.parser.parse(contents, "text/html")

    def test_extract_cusip(self):
        self.assertEqual("38259P AD4", self.results.get("cusip"))

    def test_extract_issue_name(self):
        self.assertEqual("3.375% Notes due 2024 (the  Notes )", self.results.get("issue_name"))

    def test_extract_issuer_name(self):
        pass

    def test_extract_company_address(self):
        pass


