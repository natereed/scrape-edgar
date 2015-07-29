import os

# Script for cleaning data in the daily worksheets (converted from the master file, CUSIP_db_master_file.xlsx)

def read_input_file(filename):
    f = open(filename, "rU")
    lines = f.readlines()
    f.close()
    return lines

# Normalize (strip whitespace, extra lines, etc.)
def strip_blank_lines(lines):
    result_lines = []
    blank_lines = 0
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            result_lines.append(line)
        else:
            blank_lines += 1

    stats = dict()
    stats['num_input_lines'] = len(lines)
    stats['num_lines'] = len(result_lines)
    stats['num_blank_lines'] = blank_lines
    return result_lines, stats

def is_valid_daily_issuer(line):
    tokens = line.split(',')
    #print "%d tokens " % len(tokens)
    if len(tokens) != 16:
        return False

    issuer_num = tokens[0]
    issue_check = tokens[1]

    if issuer_num == '999999':
        return False

    return issuer_num and issue_check

def is_valid_daily_issue(line):
    tokens = line.split(',')
    if len(tokens) != 17:
        return False

    issuer_num = tokens[0]
    issue_num = tokens[1]
    issue_check = tokens[2]

    if issuer_num == '999999':
        return False

    # TBD: Implement cusip validation
    # See: https://en.wikipedia.org/wiki/CUSIP#Check_digit_pseudocode
    return issuer_num and issue_num and issue_check

def print_stats(stats):
    print "Input lines: %d" % stats['num_input_lines']
    print "%d blank lines " % stats['num_blank_lines']
    print "Using %d lines " % stats['num_lines']
    print "Lines rejected: %d" % stats['rejected']

def clean(filename, validate_func):
    print "Cleaning %s" % filename
    lines = read_input_file(filename)
    lines, stats = strip_blank_lines(lines)

    if not os.path.exists("cleaned"):
        os.makedirs("cleaned")

    # Clean by removing invalid rows
    with open("cleaned/%s" % filename, "w") as out:
        stats['rejected'] = 0
        for line in lines[1:]:
            if validate_func(line):
                out.write(line)
            else:
                print "Rejecting %s" % line
                stats['rejected'] += 1

    print_stats(stats)

# Worksheet #1: Daily Issuer
clean("cusip-daily-issue.csv", is_valid_daily_issue)
clean("cusip-daily-issuer.csv", is_valid_daily_issuer)