import csv
import sys
import os

def usage():
    print "Usage: python score-items.py <path-to-file>"

if len(sys.argv) < 2:
    usage()
    sys.exit(-1)

path = sys.argv[1]
basename = os.path.basename(path)
(root, extension) = os.path.splitext(basename)
dirname = os.path.dirname(path)
scored_path = os.path.join(dirname, root + "-scored" + extension)

# The idea is to score based on the length of the fields, with the presumption that a longer
# address or issue name is more complete. If the address is missing, it could be a CUSIP from a
# document that typically does not include an address. This is still valid, but I'll assign a zero
# for ranking results:
def score(row):
    return (1 if row['address'] else 0) * (len(row['address']) + len(row['issue_name']))

fields = ['cusip', 'url', 'address', 'issuer_name', 'issue_name', 'date', 'document_name']
with open(path, "r") as input_file:
    reader = csv.DictReader(input_file)
    with open(scored_path, "w") as output_file:
        writer = csv.DictWriter(output_file, fields + ['score'])
        writer.writeheader()
        for row in reader:
            row['score'] = score(row)
            writer.writerow(row)


