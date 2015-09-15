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
        self.assertEqual(['4.121% NOTES DUE 2013'], results.get("issue_name"))

    def test_extract_multiple_cusips(self):
        contents = load_file_contents("example_filings/EX-99-multiple_convertible_notes.html")
        results = self.parser.parse(contents)
        self.assertEqual(['229678AD9', '229678AF4', '229678AH0'], results.get("cusip"))

    def test_extract_multiple_issues(self):
        contents = load_file_contents("example_filings/EX-99-multiple_convertible_notes.html")
        results = self.parser.parse(contents)
        self.assertEqual(['2.50% CONVERTIBLE SENIOR NOTES DUE 2017',
                          '1.125% CONVERTIBLE SENIOR NOTES DUE 2018',
                          '1.875% CONVERTIBLE SENIOR NOTES DUE 2020'], results.get("issue_name"))

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

    def test_broken_issue_names_from_targa_425(self):
        # See: http://www.sec.gov/Archives/edgar/data/1092914/000119312515029347/d864125d425.htm
        contents = load_file_contents("example_filings/targa_form_425.html")
        results = self.parser.parse(contents)
        self.assertEqual(['04939MAM1', '04939MAL3', '04939MAJ8'], results.get('cusip'))
        self.assertEqual(['6 5/8% SENIOR NOTES DUE 2020', '4 3/4% SENIOR NOTES DUE 2021', '5 7/8% SENIOR NOTES DUE 2023',
                          'SENIOR NOTES DUE 2018'], results.get('issue_name'))

    def test_broken_issue_names_from_microsoft(self):
        contents = load_file_contents("example_filings/EX-4.2-MSFT.html")
        results = self.parser.parse(contents)
        self.assertEqual(['1.625% NOTES DUE 2018', '3.625% NOTES DUE 2023', '4.875% NOTES DUE 2043'], results.get('issue_name'))
        self.assertEqual(['594918 AV6', '594918 AW4', '594918 AX2'], results.get('cusip'))

    def test_missing_cusips_from_fwp(self):
        contents = load_file_contents("example_filings/noble_energy_fwp.html")
        results = self.parser.parse(contents)
        self.assertEqual(['5.250% NOTES DUE 2043'], results.get('issue_name'))
        self.assertEqual(['655044AG0'], results.get('cusip'))

    def test_rejects_long_issue_names(self):
        contents = load_file_contents("example_filings/aflac_ex_4.1.html")
        results = self.parser.parse(contents)
        self.assertEqual(['3.625% SENIOR NOTES DUE 2024'], results.get("issue_name"))

    def test_home_depot_notes_breakage(self):
        # This error was caused by looking for the words "Common Stock" as the first possible match. The phrase
        # can appear in filings for other types of securities, too. Also, we need to match "Floating Rate Notes due 2017"
        # and similar phrases. Right now it's looking for a %.
        contents = load_file_contents('example_filings/hd_exhibit11x09082015.html')
        results = self.parser.parse(contents)
        self.assertEqual(['FLOATING RATE NOTES DUE 2017', '3.35% NOTES DUE 2025'], results.get("issue_name"))
