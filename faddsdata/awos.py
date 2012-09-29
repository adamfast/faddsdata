# Handle data from AWOS.txt

from parse import parse_line, convert_dashed_dms_to_float
from format_definitions.awos import AWOS_RECORDS

def parse_awos_line(line):
    "Parse a single line in the AWOS file"
    r = parse_line(line, AWOS_RECORDS)
    # Parse out useful coordinates
    if r['record_type'] == 'AWOS1':  # only if it's a record type 1
        if r['latitude']:
            r['lat'] = convert_dashed_dms_to_float(r['latitude'])
        if r['longitude']:
            r['lon'] = convert_dashed_dms_to_float(r['longitude'])
    return r

if __name__ == '__main__':
    path = '/Users/adam/Downloads/56DySubscription_November_18__2010_-_January_13__2011/'
    raw = open(path + 'AWOS.txt')

    for line in raw:
        val = parse_apt_line(line)
