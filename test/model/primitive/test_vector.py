import unittest
import math

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
from point import Point
from vector import Vector


class TestPoint(unittest.TestCase):
    def setUp(self):
        a = Point(1.2, 2.4)
        b = Point(2.2, 3.4)
        c = Point(1.2, 3.4)

        self.vec_ab = Vector(a, b)
        self.vec_ab2 = Vector(a, b)
        self.vec_ac = Vector(a, c)
    #end

    def test_basic(self):
        self.assertAlmostEqual(self.vec_ab.x, 1.0)
        self.assertAlmostEqual(self.vec_ab.y, 1.0)
    #end

    def test_str(self):
        self.assertEqual(str(self.vec_ab), "1.000 1.000")
    #end

    def test_eq(self):
        self.assertEqual(self.vec_ab==self.vec_ab2, True)
    #end

    def test_dot(self):
        dot = self.vec_ab.dot(self.vec_ac)
        self.assertAlmostEqual(dot, 1.0)
    #end

    def test_abs(self):
        self.assertAlmostEqual(self.vec_ab.abs(), math.sqrt(2.0))
    #end

    def test_calc_angle(self):
        angle = self.vec_ab.calc_angle(self.vec_ac)
        self.assertAlmostEqual(angle, 45.0/180*math.pi)
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end
