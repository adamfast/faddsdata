# Handle data from APT.txt

from format_definitions import APT_RECORDS, ATT_RECORDS, RWY_RECORDS, RMK_RECORDS

def build_list_of_lengths(definition):
    """Take a SortedDict and iterate over it, building a list of field lengths."""
    lengths = []
    for key in definition:
        lengths.append(definition[key])
    return lengths

def calculate_lengths(fields):
    count = 0
    out = []
    for i in fields:
        end = 0
        for x in range(0, count):
            end += fields[x]
        if end != 0:
            out.append(end)
        count += 1
    return out

# calculate cumulative length from the list of lengths
APT_RECORD_LENGTHS = calculate_lengths(build_list_of_lengths(APT_RECORDS))
ATT_RECORD_LENGTHS = calculate_lengths(build_list_of_lengths(ATT_RECORDS))
RWY_RECORD_LENGTHS = calculate_lengths(build_list_of_lengths(RWY_RECORDS))
RMK_RECORD_LENGTHS = calculate_lengths(build_list_of_lengths(RMK_RECORDS))

# borrowed from http://code.activestate.com/recipes/65224/
def split_at(theline, cuts, lastfield=True):
    pieces = [ theline[i:j].strip() for i, j in zip([0]+cuts, cuts) ]
    if lastfield:
        pieces.append(theline[cuts[-1]:].strip())
    return pieces

def correlate(data, definition):
    combined = {}
    count = 0
    for key in definition.keys():
        combined[key] = data[count]
        count += 1
    return combined

def parse_apt_line(line):
    if line[:3] == 'APT':
        return correlate(split_at(line, APT_RECORD_LENGTHS), APT_RECORDS)
    elif line[:3] == 'ATT':
        return correlate(split_at(line, ATT_RECORD_LENGTHS), ATT_RECORDS)
    elif line[:3] == 'RWY':
        return correlate(split_at(line, RWY_RECORD_LENGTHS), RWY_RECORDS)
    elif line[:3] == 'RMK':
        return correlate(split_at(line, RMK_RECORD_LENGTHS), RMK_RECORDS)
    else:
        raise Exception("Line type %s not recognized" % line[:3])

if __name__ == '__main__':
    path = '/Users/nelson/Downloads/56DySubscription_November_18__2010_-_January_13__2011/'
    raw = open(path + 'APT.txt')

    for line in raw:
        val = parse_apt_line(line)
        
import unittest
class ParseTests(unittest.TestCase):
    def test_build_list_of_lengths(self):
        from django.utils.datastructures import SortedDict
        self.assertEqual([], build_list_of_lengths(SortedDict()))
        self.assertEqual([3], build_list_of_lengths(SortedDict((('a', 3), ))))
        self.assertEqual([1, 2], build_list_of_lengths(SortedDict((('a', 1), ('b', 2)))))
        
    def test_calculate_lengths(self):
        self.assertEqual([], calculate_lengths(()))
        self.assertEqual([], calculate_lengths((1,)))
        self.assertEqual([1], calculate_lengths((1, 2)))
        self.assertEqual([1, 3, 6, 10], calculate_lengths((1, 2, 3, 4, 5)))
        
    def test_split_at(self):
        self.assertEqual(["abcd", "efghij"], split_at("abcdefghij", [4], lastfield = "true"))
        self.assertEqual(["ab", "cd", "e", "fghi", "j"], split_at("abcdefghij", [2, 4, 5, 9]))
        # XXX(nelson): this test seems to fail, is lastfield not working as expected?
        self.assertEqual(["abcd"], split_at("abcdefghij", [4], lastfield = "false"))
    
    def test_correlate(self):
        # XXX(nelson): could use some tests for correlate alone
        pass
    
    def test_full_parse_stack(self):
        "Test all the parser code together"
        from django.utils.datastructures import SortedDict
        definition = SortedDict((('first', 1), ('second', 2), ('third', 3), ('last', 5)))
        lengths = calculate_lengths(build_list_of_lengths(definition))
        val = correlate(split_at("abcdefghijk", lengths), definition)
        self.assertEqual("a", val["first"])
        self.assertEqual("bc", val["second"])
        self.assertEqual("def", val["third"])
        self.assertEqual("ghijk", val["last"])

# Test data from 56DySubscription_November_18__2010_-_January_13__2011
class AptTests(unittest.TestCase):
    def test_bad_line(self):
        "Test that bad input signals an error"
        self.assertRaises(Exception, parse_apt_line, "invalid input")
    
    def test_apt(self):                    
        apt = parse_apt_line('APT06721.*A   AIRPORT      LWC 11/18/2010ACENONEKSKANSAS              DOUGLAS              KSLAWRENCE                                LAWRENCE MUNI                             PUPUCITY OF LAWRENCE                   6 EAST 6TH STREET                                                       LAWRENCE, KS 66044                               785-832-3400STEVE BENNETT                      6 EAST 6TH STREET                                                       LAWRENCE, KS 66044                               785-832-312639-00-40.0000N 140440.0000N095-12-59.3000W342779.3000WE  833S04E2005    KANSAS CITY                   03N    486ZKC ZCKKANSAS CITY                                                        NICT WICHITA                                       1-800-WX-BRIEF                                                    LWC Y04/1940O                NGY    NO OBJECTION NNNY                        S S10292008        100LLA                                  MAJORMAJORHIGH    HIGH    DUSK-DAWNN123.000                                   123.000Y   CG N 049004001001   000               00210001365001680000015009/30/20083RD PARTY SURVEY07/11/20083RD PARTY SURVEY07/11/2008 HGR,TIE     AMB,INSTR,RNTL,SALES                                                   Y-LKLWC   \n')
        self.assertEqual('APT', apt['record_type'])
        self.assertEqual('LAWRENCE', apt['associated_city'])
        self.assertEqual('123.000', apt['common_traffic_advisory_frequency'])
        self.assertEqual('KLWC', apt['icao_identifier'])
        self.assertEqual('LWC', apt['location_identifier'])
        self.assertEqual('39-00-40.0000N', apt['point_latitude_formatted'])
        self.assertEqual('140440.0000N', apt['point_latitude_seconds'])

    def test_att(self):
        att = parse_apt_line('ATT06721.*A   KS 1ALL/ALL/0800-2000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          \n')
        self.assertEqual('ATT', att['record_type'])
        self.assertEqual('ALL/ALL/0800-2000', att['attendance_schedule'])
        
    def test_rwy(self):
        rwy = parse_apt_line('RWY06721.*A   KS01/19   3901  75CONC-G                      MED  01 019          NNPI  G      39-00-19.0109N 140419.0109N095-13-11.8792W342791.8792W  832.5                                                                            833P2L              Y  TREE           A(V) 27   61 187049L    19 199          NNPI  G      39-00-55.4278N 140455.4278N095-12-55.6483W342775.6483W  831.1                                                                            833P2L              Y  TREE           A(V) 34   72 268847R    3RD PARTY SURVEY07/11/2008  12.5  15.6              0.0    3RD PARTY SURVEY07/11/20083RD PARTY SURVEY07/11/2008                                                    3RD PARTY SURVEY07/11/2008                                                                                                                                                          0.0    3RD PARTY SURVEY07/11/20083RD PARTY SURVEY07/11/2008                                                    3RD PARTY SURVEY07/11/2008                                                                                                                                                                                                                                                                    \n')
        self.assertEqual('RWY', rwy['record_type'])
        self.assertEqual('06721.*A', rwy['facility_site_number'])
        self.assertEqual('01/19', rwy['runway_identification'])
        self.assertEqual('01', rwy['base_end_identifier'])
        self.assertEqual('19', rwy['reciprocal_end_identifer'])
        
    def test_rmk(self):
        rmk = parse_apt_line('RMK06721.*A   KSA81        ACTVT MIRL RYS 01/19 & 15/33; PAPI RYS 01 & 19 AND 15 & 33; REIL RYS 01 & 19; MALSR RY 33 - CTAF.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 \n')
        self.assertEqual('RMK', rmk['record_type'])
        self.assertEqual('06721.*A', rmk['facility_site_number'])
        self.assertEqual('ACTVT MIRL RYS 01/19 & 15/33; PAPI RYS 01 & 19 AND 15 & 33; REIL RYS 01 & 19; MALSR RY 33 - CTAF.',
                         rmk['element_text'])

        