#!/usr/bin/python
# -*- coding: latin-1 -*-

"Utility functions for parsing FADDS fixed width data"

import datetime

class ParseException(Exception): pass

def parse_line(data, definition):
    """Parse a line of fixed width text according to a definition, returning a dictionary of stripped tokens
    Definition is a list of tuples: ("key", width)
    
    parse_fixed_width_line("abcdefghij", (("first", 2), ("second", 3), (None, 1), ("third", 4)))
    >>> { "first": "ab", "second": "cde", "third": "ghij" }"""

    data = data.replace('\r', '').replace('\n', '')
    # Calculate the start and end of every field
    splits = []
    start = 0
    end = 0
    for width in list(zip(*definition))[1]:
        end += width
        splits.append((start, end))
        start += width

    # Check that the input line is exactly the right length, or right length plus a newline
    if not (len(data) == end):
        raise ParseException("Expected length %d, got length %d" % (end, len(data)))
    
    # Return a dictionary of each extracted field
    r = {}
    for (name, _), (start, end) in zip(definition, splits):
        if name is not None:
            r[name] = data[start:end].strip().replace('\xfa', '').replace('\xd1', 'N').replace('\xbf', '').replace('\xb4', '').replace('\xb0', '')
    return r

def convert_dms_to_float(c):
    "Convert a string coordinate like 0844402W or 335303N to a float like 33.8841666"
    assert (len(c) == 8 and c[7] in 'WE') or (len(c) == 7 and c[6] in 'NS')
    
    if len(c) == 8:
        d = int(c[0:3], 10)
        m = int(c[3:5], 10)
        s = int(c[5:7], 10)
        sign = 1
        if c[7] == 'W': sign = -1
    else:
        d = int(c[0:2], 10)
        m = int(c[2:4], 10)
        s = int(c[4:6], 10)
        sign = 1
        if c[6] == 'S': sign = -1
    return sign * (float(d) + (m*60 + s) / 3600.0)

def convert_dashed_dms_to_float(c):
    "Convert a coordinate like 37-32-29.770N to 32.49616666666667"
    
    # western and southern hemisphers
    assert(c[-1] in 'NSEW')
    sign = 1
    if c[-1] == 'W' or c[-1] == 'S':
        sign = -1
    
    d, m, s = c[:-1].split('-')
    return sign * (int(d) + (int(m) * 60 + float(s)) / 3600.0)

def convert_boolean(c):
    "Convert the Y/N from the FAA into Python True/False"
    if c == 'Y':
        return True
    return False

def convert_month_year(c):
    "Convert the MM/YYYY from the FAA into a Python Date object."
    try:
        return datetime.datetime.strptime(c, "%m/%Y").date()
    except:
        return None

def convert_date(c):
    "Convert the MM/DD/YYYY from the FAA into a Python Date object."
    try:
        return datetime.datetime.strptime(c, "%m/%d/%Y").date()
    except:
        return None

import unittest
class ParseTests(unittest.TestCase):
    def test_parse_line(self):
        # normal input
        self.assertEqual({ "first": "ab", "second": "cde", "third": "ghij" },
                         parse_line("abcdefghij", (("first", 2), ("second", 3), (None, 1), ("third", 4))))
        self.assertEqual({ "first": "a", "second": "cd" },
                         parse_line("a cd", (("first", 2), ("second", 2))))
        # normal input with a newline
        self.assertEqual({ "first": "ab", "second": "cd" },
                         parse_line("abcd\n", (("first", 2), ("second", 2))))
        # broken input
        self.assertRaises(ParseException, parse_line, "abc", (("first", 2), ("second", 2)))
        self.assertRaises(ParseException, parse_line, "abcde", (("first", 2), ("second", 2)))
       
    def test_convert_dms_to_float(self):
        self.assertAlmostEqual(33.884166666, convert_dms_to_float('335303N'))
        self.assertAlmostEqual(-33.884166666, convert_dms_to_float('335303S'))
        self.assertAlmostEqual(-84.73388888888, convert_dms_to_float('0844402W'))
        self.assertAlmostEqual(84.73388888888, convert_dms_to_float('0844402E'))        
    
    def test_convert_dashed_dms_to_float(self):
        self.assertAlmostEqual(33.884166666, convert_dashed_dms_to_float('33-53-03.000N'))
        self.assertAlmostEqual(-33.884166666, convert_dashed_dms_to_float('33-53-03.000S'))
        self.assertAlmostEqual(-84.73388888888, convert_dashed_dms_to_float('084-44-02.000W'))
        self.assertAlmostEqual(84.73388888888, convert_dashed_dms_to_float('084-44-02.000E'))
        self.assertAlmostEqual(1.016975, convert_dashed_dms_to_float('01-01-01.110N'))
