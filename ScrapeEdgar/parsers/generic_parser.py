# This is a parser designed to try to parse CUSIP's and issue names out of any document that might contain them.
# A limitation of this is that since it's intended for a much broader set of input documents, it might be more
# prone to errors, as the inputs might not have been tested before. "Garbage in, garbage", although one man's
# garbage is another random SEC filing.

#from nltk.corpus import words
from ScrapeEdgar.parsers.base_parser import BaseParser
from ScrapeEdgar.cleaning_functions import remove_duplicates
from ScrapeEdgar.cusip_utils.check_digit import validate_cusip

import re
import logging

class GenericParser(BaseParser):

    def extract_cusips(self, text):
        pat1 = re.compile(r'CUSIP\s+(no|number|num|#)*\.*:*\s*(\w{6}\W*\w{3})\b', re.IGNORECASE | re.MULTILINE)
        pat2 = re.compile(r'CUSIP\s*(no|number|num|#)*\.*(/ISIN)*:*\s*(\w{6}\W*\w{3})', re.IGNORECASE | re.MULTILINE)

        matches = re.findall(pat1, text)
        if matches:
            return self.normalize_results([match[1] for match in matches])

        matches = re.findall(pat2, text)
        if matches:
            return self.normalize_results([match[2] for match in matches])

        #return self.extract_cusips_using_nlp(text)
        return []

    #def extract_cusips_using_nlp(self, text):
    #    pat = re.compile(r'(\w{6}\s*\w{3})\b', re.IGNORECASE | re.MULTILINE)
    #    matches = re.findall(pat, text)
    #    cusips = []
    #    logging.info("%d candidates for CUSIP, comparing against dictionary words" % len(matches))
    #    for candidate in matches:
    #        print "Candidate: " + candidate
    #        if not candidate in words.words() and validate_cusip(candidate)["is_valid"]:
    #            cusips.append(candidate)

    #   return self.normalize_results(cusip for cusip in cusips)

    def normalize_string(self, string):
        string = re.sub(r'\s+', ' ', string.upper().strip())
        # Standardize pluralization
        return re.sub(r'NOTE\b', 'NOTES', string, flags=re.IGNORECASE)

    def normalize_results(self, results):
        normalized_results = map(self.normalize_string, results)
        return remove_duplicates(normalized_results)

    def extract_issue_names(self, text):
        # Common Stock
        common_stock_pat = re.compile(r'(Common Stock(, \$[0-9]+\.[0-9]+ par value per share)*)', re.IGNORECASE | re.MULTILINE)
        match = common_stock_pat.search(text)
        if match:
            return match.group(1)

        # Notes
        notes_pat = re.compile(r'([0-9]+\.*\s*[0-9/]+%\s+(Senior|Convertible|Convertible Senior){0,1}\s*Notes*\s+due\s+[0-9]{4})', re.IGNORECASE | re.MULTILINE)
        matches = re.findall(notes_pat, text)

        if matches:
            results = self.normalize_results([match[0] for match in matches])
            return results

        return None

    def parse_text(self, text, **kwargs):
        cusips = self.extract_cusips(text)
        issue_names = self.extract_issue_names(text)
        return {'cusip' : cusips, 'issue_name' : issue_names}