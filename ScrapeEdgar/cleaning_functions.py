import re
import types

__author__ = 'reedn'

# Functions for cleaning data. This is divided into sections, one for the scraper, which does a minimal amount of cleaning
# as data is collected., and one for cleaning the raw data to transform it into something suitable
# for consumption.
#
# Scraper functions:

def clean_str(str):
    str = str.replace("\n", " ")
    str = re.sub(r'\s+', ' ', str)
    return str

def format_list(list, delim=','):
    if isinstance(list, types.StringTypes):
        return list

    return ("%s " % delim).join(list)

def clean_results(results, delim=';'):
    for key in results.keys():
        val = results[key]
        if not val:
            continue
        if isinstance(val, types.StringTypes):
            val = clean_str(val)
        else:
            val = [clean_str(str) for str in val]
        results[key] = val

    if results['issue_name']:
        results['issue_name'] = format_list(results['issue_name'], delim)

    if results['cusip']:
        results['cusip'] = format_list(results['cusip'], delim)

    return results

# Remove duplicates while maintaining order:
def remove_duplicates(list_of_whatever):
    seen = {}
    result = []
    for element in list_of_whatever:
        if not seen.get(element):
            result.append(element)
            seen[element] = True
    return result

