import csv
import os

def split_csv_file(filename, size):
    # Get the fieldnames
    f = open(filename, "r")
    header = f.readline()
    f.close()
    fields = [field.strip() for field in header.split(',')]
    print "Fields: %s" % fields

    basename = os.path.splitext(filename)[0]

    # Test open file, reader
#    with open(filename, "r") as in_file:
#        reader = csv.DictReader(in_file)
 #       for row in reader:
 #           print row

    # Open input
    with open(filename, "r") as in_file:

        # Create reader for input
        reader = csv.DictReader(in_file)

        chunknum = 1
        row = None

        # Loop until no more rows are found, incrementing chunknum each time a new file is created:
        while True:
            out_filename = "%s-chunk%d.csv" % (basename, chunknum)
            with open(out_filename, "w") as out_file:
                writer = csv.DictWriter(out_file, fields)
                writer.writeheader()

                for rownum in range(size):
                    try:
                        row = reader.next()
                        writer.writerow(row)
                    except StopIteration:
                        row = None
                        break

                if not row:
                    break

                chunknum += 1

split_csv_file("/Users/reedn/ScrapeEdgar/companies.csv", 1000)