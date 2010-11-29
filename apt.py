# Handle data from APT.txt

from format_definitions import APT_RECORDS, ATT_RECORDS, RWY_RECORDS, RMK_RECORDS
from parse import build_list_of_lengths, calculate_lengths, split_at, correlate

# calculate cumulative length from the list of lengths
APT_RECORD_LENGTHS = calculate_lengths(build_list_of_lengths(APT_RECORDS))
ATT_RECORD_LENGTHS = calculate_lengths(build_list_of_lengths(ATT_RECORDS))
RWY_RECORD_LENGTHS = calculate_lengths(build_list_of_lengths(RWY_RECORDS))
RMK_RECORD_LENGTHS = calculate_lengths(build_list_of_lengths(RMK_RECORDS))

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

        