# expand.py - Converts multi-valued columns (CUSIP, ISSUE_NAME) into multiple rows
# Example: 594918AS3; 594918AT1; 594918AU8,http://www.sec.gov/Archives/edgar/data/789019/000119312513192843/d531397dex42.htm,,Microsoft Corp.,1.000% NOTES DUE 2018; 2.375% NOTES DUE 2023; 3.750% NOTES DUE 2043,05/01/2013,EX-4.2 of 8-K for MICROSOFT CORP
# This should be three rows, one for each CUSIP # above.

import csv
import sys
import os

def usage():
    print "Usage: python expand-items.py <path-to-file>"

if len(sys.argv) < 2:
    usage()
    sys.exit(-1)

path = sys.argv[1]
basename = os.path.basename(path)
(root, extension) = os.path.splitext(basename)
dirname = os.path.dirname(path)
expanded_path = os.path.join(dirname, root + "-expanded" + extension)

fields = ['cusip', 'url', 'address', 'issuer_name', 'issue_name', 'date', 'document_name']
with open(path, "r") as input_file:
    reader = csv.DictReader(input_file)
    with open(expanded_path, "w") as output_file:
        writer = csv.DictWriter(output_file, fields)
        writer.writeheader()
        for row in reader:
            cusip_numbers = row['cusip'].split(';')
            issue_names = row['issue_name'].split(';')
            for i, cusip_number in enumerate(cusip_numbers):
                row['cusip'] = cusip_number.strip()
                row['issue_name'] = issue_names[i].strip()
                writer.writerow(row)


