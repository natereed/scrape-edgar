import unittest

from cleaning_functions import clean_results

class CleaningTests(unittest.TestCase):

    def test_clean_parse_results_converts_lists_to_strings(self):
        results = {'cusip': [u'63888U108', u'6388U109'], 'issuer_name': 'Natural Grocers by Vitamin Cottage Inc',\
         'issue_name': u'Common Stock, $0.001 Par Value per share'}

        clean_results(results, ';')
        self.assertEqual(u'63888U108; 6388U109', results['cusip'])

    def test_remove_newline_from_issue_name(self):
        results = {'cusip': None, 'issue_name': u'Common Stock,\npar value $0.01 per share', 'issuer_name': 'TRW Automotive Holdings Corp.', 'address': u'12001 Tech Center Drive, Livonia, Michigan 48150'}

        clean_results(results)
