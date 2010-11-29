"Utility functions for parsing FADDS fixed width data"

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
