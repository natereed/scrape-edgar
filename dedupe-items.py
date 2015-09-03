import csv
import sys
import os

def usage():
    print "Usage: python dedupe-items.py <path-to-file>"

if len(sys.argv) < 2:
    usage()
    sys.exit(-1)

path = sys.argv[1]
basename = os.path.basename(path)
(root, extension) = os.path.splitext(basename)
dirname = os.path.dirname(path)
deduped_path = os.path.join(dirname, root + "-deduped" + extension)

cusip_to_items = dict()

fields = ['cusip', 'url', 'address', 'issuer_name', 'issue_name', 'date', 'document_name', 'score']
with open(path, "r") as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        cusip = row['cusip']
        item = cusip_to_items.get(cusip)
        if not item:
            cusip_to_items[cusip] = row
        elif item['score'] > row['score']:
            cusip_to_items[cusip] = item

with open(deduped_path, "w") as output_file:
    writer = csv.DictWriter(output_file, fields)
    writer.writeheader()
    for cusip in cusip_to_items.keys():
        item = cusip_to_items[cusip]
        print item
        writer.writerow(item)





