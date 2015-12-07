import unittest

from ScrapeEdgar.parsers.test_utils import load_file_contents
from ScrapeEdgar.parsers.parser13d import Parser13d

class Parser13dTests(unittest.TestCase):

    def setUp(self):
        self.parser = Parser13d()

    def test_nike_broken_13d_cusip_not_extracted(self):
        contents = load_file_contents('example_filings/nike_13d_broken_cusip.html')
        results = self.parser.parse(contents)
        self.assertEqual(['654106103'], results.get('cusip'))
        print results

        self.assertEqual('NIKE, Inc.', results.get('parsed_issuer_name'))