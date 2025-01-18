
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/drawing'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from multi_curve_set import MultiCurveSet

import unittest

import numpy as np
import math

class TestMultiCurveSet(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        bezier_curve = CubicBezierCurve()
        bezier_curve.append(bezier_ctrl_p)
        bezier_curve.append(bezier_ctrl_p)

        self.multi_curve_set = MultiCurveSet()
        self.multi_curve_set.append(bezier_curve)
        self.multi_curve_set.append(bezier_curve)
        self.multi_curve_set.append(bezier_curve)
    #end

    def test_init_and_getitem(self):

        bezier_curve = self.multi_curve_set[0]
        self.assertEqual(bezier_curve[0].p0.x, 0.0)
        self.assertEqual(bezier_curve[0].p0.y, 0.0)
        self.assertEqual(bezier_curve[0].p1.x, 1.0)
        self.assertEqual(bezier_curve[0].p1.y, 2.0)
        self.assertEqual(bezier_curve[0].p2.x, 10.0)
        self.assertEqual(bezier_curve[0].p2.y, 20.0)
        self.assertEqual(bezier_curve[0].p3.x, 100.0)
        self.assertEqual(bezier_curve[0].p3.y, 200.0)
    #end

    def test_len(self):
        self.assertEqual(len(self.multi_curve_set), 3)
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

