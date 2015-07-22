import unittest

from ScrapeEdgar.parsers.parser8kEx402 import Parser8kEx402
from ScrapeEdgar.parsers.test_utils import load_file_contents

# See http://www.sec.gov/Archives/edgar/data/1288776/000119312514066560/d681994dex402.htm
# Saved to ScrapeEdgar/ScrapeEdgar/parsers/example_filings/google_8k_ex4.02.html

class Parser8kEx402Tests(unittest.TestCase):
    def setUp(self):
        self.parser = Parser8kEx402()
        contents = load_file_contents("example_filings/google_8k_ex4.02.html")
        self.results = self.parser.parse(contents, "text/html", "GOOGLE INC")

    def test_extract_cusip(self):
        self.assertEqual("38259P AD4", self.results.get("cusip"))

    def test_extract_issue_name(self):
        self.assertEqual("3.375% Notes due 2024", self.results.get("issue_name"))


