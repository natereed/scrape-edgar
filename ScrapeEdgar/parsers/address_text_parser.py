import logging
import re

def format_address(address):
    address = re.sub(r'\s{2,}', ', ', address)
    address = address.replace('\n', ' ')
    return address

def parse_address(text):
    address = None
    address_pat1 = re.compile("Principal Executive Offices*:\W*([\w|\W]*)Item 2\.*\s*\(a\)",
                                 re.IGNORECASE | re.MULTILINE)

    address_pat2 = re.compile("Address\s+of\s+Issuer'*\s*s\s+Principal\s+Executive\s+Offices\s+([\w|\W]*?)Item*\s+2\.*\s*\(a\)",
                              re.IGNORECASE | re.MULTILINE)
    # This uses a dashed-line divider (-+):
    address_pat3 = re.compile(r'Principal Executive Offices:\s+-+([\w\W]+)Item 2',
                              re.IGNORECASE | re.MULTILINE)

    match = None
    patterns = [address_pat1, address_pat2, address_pat3]
    for pat in patterns:
        match = pat.search(text)
        if match:
            break

    if match:
        address = match.group(1).strip()
        address = format_address(address)
    else:
        logging.warning("No match for address")

    return address
