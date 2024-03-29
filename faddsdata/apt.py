# Handle data from APT.txt

from faddsdata.format_definitions import APT_RECORD_MAP
from faddsdata.parse import parse_line, convert_dashed_dms_to_float, convert_boolean

def parse_apt_line(line):
    "Parse a single line in the APT file"
    record_type = line[:3]
    r = parse_line(line, APT_RECORD_MAP[record_type])
    # Parse out useful coordinates
    if (record_type == 'APT'):
        r['lat'] = convert_dashed_dms_to_float(r['point_latitude_formatted'])
        r['lon'] = convert_dashed_dms_to_float(r['point_longitude_formatted'])
        r['control_tower'] = convert_boolean(r['control_tower'])
    if (record_type == 'RWY'):
        if r.get('base_end_latitude_physical_runway_end_formatted', False):
            r['base_end_lat'] = convert_dashed_dms_to_float(r['base_end_latitude_physical_runway_end_formatted'])
        if r.get('base_end_longitude_physical_runway_end_formatted', False):
            r['base_end_lon'] = convert_dashed_dms_to_float(r['base_end_longitude_physical_runway_end_formatted'])
        if r.get('base_end_latitude_displaced_threshold_formatted', False):
            r['base_end_displaced_threshold_lat'] = convert_dashed_dms_to_float(r['base_end_latitude_displaced_threshold_formatted'])
        if r.get('base_end_longitude_displaced_threshold_formatted', False):
            r['base_end_displaced_threshold_lon'] = convert_dashed_dms_to_float(r['base_end_longitude_displaced_threshold_formatted'])
        if r.get('reciprocal_end_latitude_physical_runway_end_formatted', False):
            r['reciprocal_end_lat'] = convert_dashed_dms_to_float(r['reciprocal_end_latitude_physical_runway_end_formatted'])
        if r.get('reciprocal_end_longitude_physical_runway_end_formatted', False):
            r['reciprocal_end_lon'] = convert_dashed_dms_to_float(r['reciprocal_end_longitude_physical_runway_end_formatted'])
        if r.get('reciprocal_end_latitude_physical_runway_end_formatted', False):
            r['reciprocal_end_displaced_threshold_lat'] = convert_dashed_dms_to_float(r['reciprocal_end_latitude_physical_runway_end_formatted'])
        if r.get('reciprocal_end_longitude_physical_runway_end_formatted', False):
            r['reciprocal_end_displaced_threshold_lon'] = convert_dashed_dms_to_float(r['reciprocal_end_longitude_physical_runway_end_formatted'])
    return r

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
        apt = parse_apt_line('APT06721.*A   AIRPORT      LWC 10/17/2013ACENONEKSKANSAS              DOUGLAS              KSLAWRENCE                                LAWRENCE MUNI                                     PUPUCITY OF LAWRENCE                   6 EAST 6TH STREET                                                       LAWRENCE, KS 66044                               785-832-3400STEVE BENNETT                      6 EAST 6TH STREET                                                       LAWRENCE, KS 66044                               785-832-312639-00-40.0000N 140440.0000N095-12-59.3000W342779.3000WE  833.3S04E2005    KANSAS CITY                   03N    486ZKC ZCKKANSAS CITY                                                        NICT WICHITA                                       1-800-WX-BRIEF                                                    LWC Y04/1940O                NGY    NO OBJECTION NNNYS S05242013        100LLA                                  MAJORMAJORHIGH    HIGH    SEE RMKSS-SR  N123.000123.000Y   CG N 049004001001   000               00210001365001680000015004/30/20133RD PARTY SURVEY08/28/20103RD PARTY SURVEY08/28/2010 HGR,TIE     AMB,INSTR,RNTL,SALES                                                   Y-LKLWC                                                                                                                                                                                                                                                                                                                           \n')
        self.assertEqual('APT', apt['record_type'])
        self.assertEqual('LAWRENCE', apt['associated_city'])
        self.assertEqual('123.000', apt['common_traffic_advisory_frequency'])
        self.assertEqual('KLWC', apt['icao_identifier'])
        self.assertEqual('LWC', apt['location_identifier'])
        self.assertEqual('39-00-40.0000N', apt['point_latitude_formatted'])
        self.assertEqual('140440.0000N', apt['point_latitude_seconds'])
        self.assertEqual('049', apt['singles_based'])
        self.assertAlmostEqual(39.01111111, apt['lat'])

    def test_att(self):
        att = parse_apt_line('ATT06721.*A   KS 1ALL/ALL/0800-2000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      \n')
        self.assertEqual('ATT', att['record_type'])
        self.assertEqual('ALL/ALL/0800-2000', att['attendance_schedule'])
        
    def test_rwy(self):
        rwy = parse_apt_line('RWY06721.*A   KS01/19   3901  75CONC-G                      MED  01 019          NNPI  G39-00-19.0108N 140419.0108N095-13-11.8792W342791.8792W  832.5 403.50                                                                   833.3P2L              Y                 A(V) 50                 19 199          NNPI  G39-00-55.4275N 140455.4275N095-12-55.6484W342775.6484W  831.0 403.50                                                                   833.3P2L              Y  TREE           A(V) 34   72 268370L    3RD PARTY SURVEY08/28/2010  12.5  15.6              0.0    3RD PARTY SURVEY08/28/20103RD PARTY SURVEY08/28/2010                                                    3RD PARTY SURVEY08/28/2010                                                                                                                                                          0.0    3RD PARTY SURVEY08/28/20103RD PARTY SURVEY08/28/2010                                                    3RD PARTY SURVEY08/28/2010                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            \n')
        self.assertEqual('RWY', rwy['record_type'])
        self.assertEqual('06721.*A', rwy['facility_site_number'])
        self.assertEqual('01/19', rwy['runway_identification'])
        self.assertEqual('01', rwy['base_end_identifier'])
        self.assertEqual('19', rwy['reciprocal_end_identifer'])
        
    def test_rmk(self):
        rmk = parse_apt_line('RMK06721.*A   KSA81-APT      ACTVT MIRL RYS 01/19 & 15/33; PAPI RYS 01 & 19 AND 15 & 33; REIL RYS 01 & 19; MALSR RY 33 - CTAF.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           \n')
        self.assertEqual('RMK', rmk['record_type'])
        self.assertEqual('06721.*A', rmk['facility_site_number'])
        self.assertEqual('ACTVT MIRL RYS 01/19 & 15/33; PAPI RYS 01 & 19 AND 15 & 33; REIL RYS 01 & 19; MALSR RY 33 - CTAF.',
                         rmk['element_text'])
