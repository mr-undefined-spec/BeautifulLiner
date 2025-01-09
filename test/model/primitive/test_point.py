
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
from point import Point

import unittest

import math

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.p = Point(1.2, 2.4)
        self.p2 = Point(1.2, 2.4)
        self.p3 = Point(2.2, 2.4)
        self.p4 = Point(2.2, 3.4)
    #end

    def test_basic(self):
        self.assertAlmostEqual(self.p.x, 1.2)
        self.assertAlmostEqual(self.p.y, 2.4)
    #end

    def test_str(self):
        self.assertEqual(str(self.p), "1.200 2.400")
    #end

    def test_eq(self):
        self.assertEqual(self.p==self.p2, True)
        self.assertEqual(self.p==self.p3, False)
    #end

    def test_distance(self):
        self.assertEqual(self.p.distance(self.p4), math.sqrt(2))
    #end

    def test_midpoint(self):
        midpoint = self.p.get_midpoint(self.p4)
        self.assertAlmostEqual(midpoint.x, 1.7)
        self.assertAlmostEqual(midpoint.y, 2.9)
    #end

    def test_errorRaise(self):
        with self.assertRaises(TypeError) as e:
            error = Point(None, None)
        #end with
        self.assertEqual(e.exception.args[0], 'float() argument must be a string or a real number, not \'NoneType\'')
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end
