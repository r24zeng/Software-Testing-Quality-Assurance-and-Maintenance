import unittest
from a1q3 import M


class CoverageTests(unittest.TestCase):
    def test_1(self):
        """Comment"""
        o = M()
        # test path [1, 2, 3, 4, 10, 12, 13]
        o.m('', 0)
        # test path [1, 2, 3, 5, 6, 10, 11, 13]
        o.m('l', 0)
        # test path [1, 2, 3, 5, 7, 8, 10, 11, 13]
        o.m('li', 0)
        # test path [1, 2, 3, 5, 7, 9, 10, 11, 13]
        o.m('live', 0)
        pass

    def test_2(self):
        """Comment"""
        o = M()
        # test path [1, 2, 3, 4, 10, 12, 13]
        o.m('', 0)
        # test path [1, 3, 5, 6, 10, 11, 13]
        o.m('l', 5)
        # test path [1, 3, 5, 7, 8, 10, 11, 13]
        o.m('li', 5)
        # test path [1, 3, 5, 7, 9, 10, 11, 13]
        o.m('live', 5)
        pass

    def test_3(self):
        """Comment"""
        o = M()
        # test path [1, 2, 3, 4, 10, 12, 13]
        o.m('', 0)
        # test path [1, 3, 5, 6, 10, 11, 13]
        o.m('l', 5)
        # test path [1, 3, 4, 10, 12, 13]
        o.m('', 5)
        # test path [1, 2, 3, 5, 7, 8, 10, 11, 13]
        o.m('li', 5)
        # test path [1, 2, 3, 5, 7, 9, 10, 11, 13]
        o.m('live', 5)
        pass

    def test_4(self):
        """Comment"""
        o = M()
        # test path [1, 2, 3, 4, 10, 12, 13]
        o.m('', 0)
        # test path [1, 3, 4, 10, 12, 13]
        o.m('', 5)
        # test path [1, 2, 3, 5, 6, 10, 11, 13]
        o.m('l', 0)
        # test path [1, 3, 5, 6, 10, 11, 13]
        o.m('l', 5)
        # test path [1, 2, 3, 5, 7, 8, 10, 11, 13]
        o.m('li', 0)
        # test path [1, 3, 5, 7, 8, 10, 11, 13]
        o.m('li', 5)
        # test path [1, 2, 3, 5, 7, 9, 10, 11, 13]
        o.m('live', 0)
        # test path [1, 3, 5, 7, 9, 10, 11, 13]
        o.m('live', 5)
        pass

