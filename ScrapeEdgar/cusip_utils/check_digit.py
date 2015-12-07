import re
import logging

# See: https://en.wikipedia.org/wiki/CUSIP#Check_digit_pseudocode
def validate_cusip(cusip):
    cusip = re.sub("\s+", "", cusip)

    if len(cusip) != 9:
        return {'is_valid': False, 'reason': 'Cusip not correct length. Input: %s' % cusip}

    checksum_digit = cusip[8]
    if not checksum_digit.isdigit():
        return {'is_valid': False, 'reason' : 'Checksum digit must be number!'}

    cusip = cusip[:8]

    sum = 0
    for i in range(8):
        v = 0
        c = cusip[i]
        if c.isdigit():
            v = int(c)
        elif c.isalpha():
            # ordinal value of letter, eg. A = 1, B = 2
            p = ord(c) - 64 # ord("A") = 65, so p = 1
            v = p + 9
        elif c == '*':
            v = 36
        elif c == "@":
            v = 37
        elif c == "#":
            v = 38
        if (i + 1) % 2 == 0:
            v = v * 2

        sum = sum + int(v / 10) + v % 10

    checksum = (10 - (sum % 10)) % 10

    if checksum != int(checksum_digit):
        return {'is_valid' : False, 'reason': 'Invalid checksum'}

    logging.debug("CUSIP #%s   checksum: %s    check digit: %s" % (cusip, checksum, checksum_digit))
    return {'is_valid' : True}






