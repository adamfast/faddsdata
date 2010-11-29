# Handle data from NATFIX.txt

from parse import parse_line

# NATFIX is defined with many 1 column wide blank spaces. We roll that in to a field and rely on strip() to clean it up
NATFIX_RECORDS = ((None, 2),
                  ("id", 6),
                  ("latitude", 8),
                  ("longitude", 9),
                  (None, 1),
                  ("artcc_id", 4),
                  ("state_code", 3),
                  ("fix_navaid_type", 7))

def parse_natfix_line(line):
    return parse_line(line[:-1], NATFIX_RECORDS)

def parse_natfix_file(fp):
    # Skip the preamble two lines
    assert fp.readline().strip() == "NATFIX"
    fp.readline()
    r = []
    for line in fp:
        if line[0] == '$':
            break
        # XXX(nelson): should probably use an iterator or do useful work instead of making a giant list
        r.append(parse_natfix_line(line))
    return r

if __name__ == '__main__':
    path = '/Users/nelson/Downloads/56DySubscription_November_18__2010_-_January_13__2011/'
    raw = open(path + 'NATFIX.txt')
    natfixes = parse_natfix_file(raw)
    print "%d records found in NATFIX.txt" % len(natfixes)
        
import unittest
# Test data from 56DySubscription_November_18__2010_-_January_13__2011
class NatfixTests(unittest.TestCase):
    def test_bad_line(self):
        "Test that bad input signals an error"
        self.assertRaises(Exception, parse_natfix_line, "invalid input")
    
    def test_natfix_line(self):
        natfix = parse_natfix_line("I SUNOL 373620N 1214837W 'ZOA CA REP-PT \n")
        for (expected, key) in (('SUNOL', 'id'),
                                ('373620N', 'latitude'),
                                ('1214837W', 'longitude'),
                                ('ZOA', 'artcc_id'),
                                ('CA', 'state_code'),
                                ('REP-PT', 'fix_navaid_type')):
            self.assertEqual(expected, natfix[key])
    
    def test_natfix_file(self):
        from StringIO import StringIO
        test_file = StringIO("""NATFIX                                  
'20101118                               
I 00A   400415N 0745601W 'ZDC PA ARPT   
I 00AK  595122N 1514147W 'ZAN AK ARPT   
$                                       
""")
        natfixes = parse_natfix_file(test_file)
        self.assertEqual(2, len(natfixes))
        self.assertEqual('ZDC', natfixes[0]["artcc_id"])
        
        