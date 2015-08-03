import csv
import os
import sys

from ScrapeEdgar.cusip_utils.check_digit import validate_cusip

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

def validate_row(row):
    if not row['cusip']:
        return {'is_valid' : False, 'reason' : 'No CUSIP #'}

    result = validate_cusip(row['cusip'])
    if not result['is_valid']:
        return result

    if not row['issue_name']:
        return {'is_valid' : False, 'reason' : 'No issue name'}

    if len(row['issue_name']) > 200:
        return {'is_valid' : False, 'reason' : 'Issue name is suspiciously long'}

    return {'is_valid' : True}

def init_rejected():
    with open(rejected_path, "w") as rejected_items_csv:
        writer = csv.DictWriter(rejected_items_csv, fields + ['reason'])
        writer.writeheader()

def init_cleaned():
    with open(cleaned_path, "w") as cleaned_items_csv:
        writer = csv.DictWriter(cleaned_items_csv, fields)
        writer.writeheader()

def write_rejected(row):
    with open(rejected_path, "a") as rejected_items_csv:
        writer = csv.DictWriter(rejected_items_csv, fields + ['reason'])
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
        validation_result = validate_row(row)
        if validation_result['is_valid']:
            write_cleaned(row)
        else:
            row['reason'] = validation_result['reason']
            write_rejected(row)



