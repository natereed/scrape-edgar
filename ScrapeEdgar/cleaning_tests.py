import unittest

from cleaning_functions import clean_scraped_data

class CleaningTests(unittest.TestCase):

    def test_clean_parse_results_converts_lists_to_strings(self):
        results = {'cusip': [u'63888U108', u'6388U109'], 'issuer_name': 'Natural Grocers by Vitamin Cottage Inc',\
         'issue_name': u'Common Stock, $0.001 Par Value per share'}

        clean_scraped_data(results, ';')
        self.assertEqual(u'63888U108; 6388U109', results['cusip'])

    def test_remove_newline_from_issue_name(self):
        results = {'cusip': None, 'issue_name': u'Common Stock,\npar value $0.01 per share', 'issuer_name': 'TRW Automotive Holdings Corp.', 'address': u'12001 Tech Center Drive, Livonia, Michigan 48150'}

        clean_scraped_data(results)

    def test_a_list_of_none_values_is_ok(self):
        results = {'cusip': [None], 'issue_name': [None], 'address' : [None]}
        clean_scraped_data(results)
        print results
        self.assertFalse(results.get('cusip'))
        self.assertFalse(results.get('issue_name'))
