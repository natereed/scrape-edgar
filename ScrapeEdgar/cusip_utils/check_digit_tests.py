import unittest
from ScrapeEdgar.cusip_utils.check_digit import validate_cusip

class CleaningTests(unittest.TestCase):
    def test_check_valid_cusip(self):
        self.assertTrue(validate_cusip("19421R200")['is_valid'])

    def test_check_invalid_cusip(self):
        self.assertFalse(validate_cusip("NUMBER FOR")['is_valid'])

    def test_check_ensco_cusip_is_invalid(self):
        self.assertFalse(validate_cusip("26874Q109"))['is_valid']
