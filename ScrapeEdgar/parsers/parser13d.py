import re
import logging

from ScrapeEdgar.parsers.base_parser import BaseParser

class Parser13d(BaseParser):
    # Optional statement that may appear after "(Amendment No...)*"
    RULE_13D_PAT = r'(Information\s+to\s+be\s+included\s+in\s+statements\s+filed\s+pursuant\s+to\s+Rule\s+13d-1\s+\(b\)\s+\(c\)\s+and\s+\(d\)\s+and\s+Amendments\s+thereto\s+filed\s+pursuant\s+to\s+Rule\s+13d-2\s+\(b\)\.)?'
    AMENDMENT_NO_FIELD_PAT = r'\(Amendment\s+No\.*:*\s+[\w\W]*?\)\*?'
    RULE_13D_FIELD_PAT = r'(\(RULE\s+13d-102\))?'
    SEC_ACT_PAT = r'(Under\s+the\s+Securities\s+Exchange\s+Act\s+of\s+1934\s+)?'
    DASHED_LINE_PAT = r'-*'
    ISSUER_NAME_CAPTURE_GROUP = r'([\w\W]+?)'
    NAME_OF_ISSUER_FIELD_PAT = r'\(Name\s+of\s+Issuer\)'
    ISSUER_NAME_PATTERN1 = AMENDMENT_NO_FIELD_PAT \
                           + r'\s+' + RULE_13D_FIELD_PAT \
                           + r'\s*' + RULE_13D_PAT \
                           + r'\s*' + SEC_ACT_PAT \
                           + DASHED_LINE_PAT \
                           + r'\s*' + ISSUER_NAME_CAPTURE_GROUP \
                           + r'\s+' + NAME_OF_ISSUER_FIELD_PAT

    def extract_issue_name(self, text):
        # Extract ISSUE NAME
        issue_name = None
        pat = re.compile(r"\(Name\s+of\s+Issuer\)([a-z0-9\.%'\s\,\$]+)-*\s+\(Title\s+of\s+Class\s+of\s+Securities\)",
                         re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            issue_name = match.group(1).strip()
            return issue_name

        pat = re.compile(r'Title\s+of\s+Class\s+of\s+Securities:\s+([\w\W]+?)\s+((Item\s+2\(e\))\.*\s+)?CUSIP\s+Number:', re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            issue_name = match.group(1).strip()
            return issue_name

        return issue_name

    def extract_issuer_name(self, text):
        # Extract Issuer
        # Check which pattern to use. This may seem redundant, but it's an optimization to avoid searching for a
        # non-match to capture groups, which in some cases, may take significant running time (~20 secs observed in one
        # case).
        issuer_name = None
        if re.search(Parser13d.NAME_OF_ISSUER_FIELD_PAT, text, re.IGNORECASE | re.MULTILINE):
            pat = re.compile(Parser13d.ISSUER_NAME_PATTERN1, re.IGNORECASE | re.MULTILINE)
            match = pat.search(text)
            if match:
                issuer_name = match.group(4).strip()
        else:
            pat = re.compile(r'Item\s+1\(a\)\.*\s*-*\s*Name\s+of\s+Issuer:([\w\W]+?)Item', re.IGNORECASE | re.MULTILINE)
            match = pat.search(text)
            if match:
                issuer_name = match.group(1).strip()
        return issuer_name

    def parse_text(self, text, **kwargs):
        cusip_number = None
        address = None

        # CUSIP
        pat = re.compile(r'\(Title\s+of\s+Class\s+of\s+Securities\)\s+([\w\W]+)\s+\(cusip\s+(no|number|num|#)\)', re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            cusip_number = match.group(1).strip()
        else:
            logging.warning("No match for cusip #")

        # Address
        pat = re.compile(r'\(Cusip\s+Number\)\s+([\w\W]+)\s+\(Name,\s+Address', re.IGNORECASE | re.MULTILINE)
        match = pat.search(text)
        if match:
            address = match.group(1).strip()
            address = re.sub(r'\s{2,}', ', ', address)
            address = address.replace('\n', ' ')
        else:
            logging.warning("No match for address")

        # Issue Name
        #pat = re.compile(r'\(Name of Issuer\)([\w\W]+)\(Title of Class of Securities\)', re.IGNORECASE | re.MULTILINE)
        #match = pat.search(text)
        #if match:
        #    issue_name = match.group(1).strip()
        #else:
        #    logging.warning("No match for issue name")
        issue_name = self.extract_issue_name(text)

        # Issuer Name
        #issuer_name = None
        #pat = re.compile(r"\(Amendment\s+No\.\s+[0-9]?\)\*?\s+([\w\W]+)\(Name\s+of\s+Issuer\)", re.IGNORECASE | re.MULTILINE)

        #match = pat.search(text)
        #print "--- match"
        #print match

        #if match:
        #    print "Match!"
        #    issuer_name = match.group(1).strip()

        issuer_name = self.extract_issuer_name(text)
        print "issuer name: %s" % issuer_name
        return {'cusip': cusip_number, 'address': address, 'issuer_name' : issuer_name, 'issue_name' : issue_name}
