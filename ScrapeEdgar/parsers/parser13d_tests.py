import unittest

from ScrapeEdgar.parsers.test_utils import load_file_contents
from ScrapeEdgar.parsers.parser13d import Parser13d

class Parser13dTests(unittest.TestCase):

    def setUp(self):
        self.parser = Parser13d()

    @unittest.skip("skipping")
    def test_nike_broken_13d_cusip_not_extracted(self):
        contents = load_file_contents('example_filings/nike_13d_broken_cusip.html')
        results = self.parser.parse(contents)
        print results

        self.assertEqual(['654106103'], results.get('cusip'))
        self.assertEqual('NIKE, Inc.', results.get('issuer_name'))
        self.assertEqual('Philip H. Knight, One Bowerman Drive, Beaverton, Oregon 97005, (503) 671-3500', results.get('address'))
        self.assertEqual('Class B Common Stock', results.get('issue_name'))

    def test_broken_aes_corp_caused_cleaning_error(self):
        contents = load_file_contents("example_filings/aes_corp_13da.html")
        results = self.parser.parse(contents)
        print results

        self.assertEqual('The AES Corporation', results.get('issuer_name'))
        self.assertEqual('Common Stock,\nPar Value $0.01 Per Share', results.get('issue_name'))
        self.assertEqual('00130H-10-5', results.get('cusip'))
