import csv
import os
import sys
import re

from ScrapeEdgar.cusip_utils.check_digit import validate_cusip

MULTI_VALUE_DELIMITTER = ';'

def usage():
    print "Usage: python clean-items.py <path-to-file>"

if len(sys.argv) < 2:
    usage()
    sys.exit(-1)

path = sys.argv[1]
basename = os.path.basename(path)
(root, extension) = os.path.splitext(basename)
dirname = os.path.dirname(path)
rejected_path = os.path.join(dirname, root + "-rejected" + extension)
cleaned_path = os.path.join(dirname, root + "-cleaned" + extension)

print "Cleaning and generating %s, %s " % (cleaned_path, rejected_path)
print "getwd: " + os.getcwd()


fields = ['cusip', 'url', 'address', 'issuer_name', 'issue_name', 'date', 'document_name']

def clean_address(row):
    row['address'] = row['address'].strip()
    row['address'] = re.sub(',+', ',', row['address'])

    if len(row['address']) > 75:
        print "-------------------------------------"
        print "Address longer than 70. Modifying address %s" % row['address']
        #tokens = row['address'].split(',')
        # Generally there are three address components, which were generated when we parsed the file and joined
        # the lines containing the address:
        #print "Getting first three tokens..."
        #row['address'] = ','.join(tokens[:3]).strip()
        #print "New address: " + row['address']

        # Check for "... Item 2,"
        match = re.search(r'(.*?),\s+Item 2', row['address'], flags=re.IGNORECASE)
        if match:
            print "Found the ... Item 2 pattern"
            row['address'] = match.group(1).strip()
            print "New address: " + row['address']

        # Check for "... offices are located at " pattern
        match = re.search("offices*\ (of the Company )*(are|is) located at,*\s+(.*)", row['address'], flags=re.IGNORECASE)
        if match:
            print "Found the located at pattern"
            row['address'] = match.group(3).strip()
            print "New address: " + row['address']

        match = re.search("offices* (are|is):*\s*(.*)", row['address'], flags=re.IGNORECASE)
        if match:
            print "Found the 'offices are/is:' pattern"
            row['address'] = match.group(2).strip()
            print "New address: " + row['address']

        # Check for dashed line ending
        match = re.search('(-+$)', row['address'])
        if match:
            print "Found the dashed line divider"
            row['address'] = row['address'].replace(match.group(1), "").strip()
            print "New address: " + row['address']
        match = re.search("Address,*\s+of\s+Issuer'*\s*s\s+Principal\s+Executive\s+Offices(.*)", row['address'], flags=re.IGNORECASE)

        # Remove redundant "Address of Issuer's..."
        if match:
            print "Found redundant descriptive text in the address"
            row['address'] = match.group(1).strip()
            print "New address: " + row['address']

        # Remove any beginning or ending punctuation
        match = re.search('^[,\.;]*\s*(.*?)[,\.;]*$', row['address'])
        if match:
            print "Removing ending punctuation"
            row['address'] = match.group(1).strip()
            print "New address: " + row['address']
    else:
        return

    print "New address: %s" % row['address']

def clean_row(row):
    clean_address(row)

def validate_row(row):
    if not row['cusip']:
        return {'is_valid' : False, 'reason' : 'No CUSIP #'}

    cusips = row['cusip'].split(MULTI_VALUE_DELIMITTER)
    for cusip in cusips:
        result = validate_cusip(cusip)
        if not result['is_valid']:
            return result

    if not row['issue_name']:
        return {'is_valid' : False, 'reason' : 'No issue name'}

    if len(row['issue_name']) > 200:
        return {'is_valid' : False, 'reason' : 'Issue name is suspiciously long'}

    issue_names = row['issue_name'].split(MULTI_VALUE_DELIMITTER)
    cusips = row['cusip'].split(MULTI_VALUE_DELIMITTER)
    if len(cusips) > len(issue_names):
        return {'is_valid' : False, 'reason' : "Insufficient issue names for given CUSIP #'s"}

    # Validate the address. This would be a good place to add a call to an address validation library, if
    # we had one. The cleaning should have taken care of most address parsing problems.
    # For now, just reject really long addresses.

    if len(row['address']) > 150:
        return {'is_valid' : False, 'reason' : 'Invalid address!'}

    return {'is_valid' : True}

def init_rejected():
    with open(rejected_path, "w") as rejected_items_csv:
        writer = csv.DictWriter(rejected_items_csv, fields + ['input_address', 'reason'])
        writer.writeheader()

def init_cleaned():
    with open(cleaned_path, "w") as cleaned_items_csv:
        writer = csv.DictWriter(cleaned_items_csv, fields)
        writer.writeheader()

def write_rejected(row):
    with open(rejected_path, "a") as rejected_items_csv:
        writer = csv.DictWriter(rejected_items_csv, fields + ['input_address', 'reason'])
        writer.writerow(row)

def write_cleaned(row):
    with open(cleaned_path, "a") as cleaned_items_csv:
        writer = csv.DictWriter(cleaned_items_csv, fields)
        writer.writerow(row)

init_rejected()
init_cleaned()

with open(path, "r") as items_csv:
    items_reader = csv.DictReader(items_csv)

    for row in items_reader:
        original_row = dict(row)
        clean_row(row)
        validation_result = validate_row(row)
        if validation_result['is_valid']:
            write_cleaned(row)
        else:
            reason = validation_result['reason']
            original_row['reason'] = reason
            original_row['input_address'] = row['address']
            write_rejected(original_row)



