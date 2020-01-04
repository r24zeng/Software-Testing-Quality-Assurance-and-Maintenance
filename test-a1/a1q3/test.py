import sys
import unittest

if __name__ == '__main__':
    name = 'a1q3.coverage_tests'
    suite = unittest.defaultTestLoader.loadTestsFromNames ([name])
    result = unittest.TextTestRunner().run (suite)
