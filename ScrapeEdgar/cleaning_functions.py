import re
import types

__author__ = 'reedn'

# Functions for cleaning data. This is divided into sections, one for the scraper, which does a minimal amount of cleaning
# as data is collected., and one for cleaning the raw data to transform it into something suitable
# for consumption.
#
# Scraper functions:

def clean_str(str):
    if not str:
        return None

    str = str.replace("\n", " ")
    str = re.sub(r'\s+', ' ', str)
    return str

def format_list(list, delim=','):
    if isinstance(list, types.StringTypes):
        return list

    if None in list:
        list.remove(None)

    return ("%s " % delim).join(list)

def clean_scraped_data(results, delim=';', max_field_length=100000):
    # Note: the csv field limit on my system is 131072, so this should provide enough
    # buffer to write out most of the field yet stay within the limit imposed by csv.
    for key in results.keys():
        val = results[key]
        if not val:
            continue
        if isinstance(val, types.StringTypes):
            val = clean_str(val)
        else:
            val = [clean_str(str) for str in val]
        results[key] = val

    if results.get('issue_name'):
        results['issue_name'] = format_list(results['issue_name'], delim)

    if results.get('cusip'):
        results['cusip'] = format_list(results['cusip'], delim)

    # Limit length
    for key in results.keys():
        if results[key]:
            results[key] = results[key][:max_field_length]

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

