import unittest

"""Simple script to run all unit tests.
Easier to run via IDE or "python2.6 -m unittest", but for Python 2.5 this may be helpful."""

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for module in ("apt",):
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(module))
    unittest.TextTestRunner().run(suite)    