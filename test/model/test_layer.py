
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))

from point import Point
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint
from curve import CubicBezierCurve
from curve import LinearApproximateCurve

from layer import Layer

import unittest

class TestLayer(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        bezier_curve = CubicBezierCurve()
        bezier_curve.append(bezier_ctrl_p)
        bezier_curve.append(bezier_ctrl_p)

        self.bezier_layer = Layer()
        self.bezier_layer.append(bezier_curve)
        self.bezier_layer.append(bezier_curve)

        lin_p0 = Point(0.0, 0.0)
        lin_p1 = Point(1.0, 1.0)
        lin_p2 = Point(1.0, 0.0)
        lin_p3 = Point(0.0, 1.0)
        lin_p4 = Point(2.0, 1.0)

        linear_ctrl_p_0_1 = LinearApproximateCurveControlPoint(lin_p0, lin_p1)
        linear_ctrl_p_2_3 = LinearApproximateCurveControlPoint(lin_p2, lin_p3)
        linear_ctrl_p_2_4 = LinearApproximateCurveControlPoint(lin_p2, lin_p4)

        linear_curve = LinearApproximateCurve()
        linear_curve.append(linear_ctrl_p_0_1)
        linear_curve.append(linear_ctrl_p_2_3)
        linear_curve.append(linear_ctrl_p_2_4)

        self.linear_layer = Layer()
        self.linear_layer.append(linear_curve)
        self.linear_layer.append(linear_curve)
    #end

    def test_init_segment_set(self):
        self.assertEqual(self.linear_layer[0][0].s.x, 0.0)
        self.assertEqual(self.linear_layer[0][0].s.y, 0.0)
        self.assertEqual(self.linear_layer[0][0].e.x, 1.0)
        self.assertEqual(self.linear_layer[0][0].e.y, 1.0)

        self.assertEqual(self.linear_layer[0][1].s.x, 1.0)
        self.assertEqual(self.linear_layer[0][1].s.y, 0.0)
        self.assertEqual(self.linear_layer[0][1].e.x, 0.0)
        self.assertEqual(self.linear_layer[0][1].e.y, 1.0)
    #end

    def test_init_cubic_bezier_curve_set(self):
        self.assertEqual(self.bezier_layer[0][0].p0.x, 0.0)
        self.assertEqual(self.bezier_layer[0][0].p0.y, 0.0)
        self.assertEqual(self.bezier_layer[0][0].p1.x, 1.0)
        self.assertEqual(self.bezier_layer[0][0].p1.y, 2.0)
        self.assertEqual(self.bezier_layer[0][0].p2.x, 10.0)
        self.assertEqual(self.bezier_layer[0][0].p2.y, 20.0)
        self.assertEqual(self.bezier_layer[0][0].p3.x, 100.0)
        self.assertEqual(self.bezier_layer[0][0].p3.y, 200.0)
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

