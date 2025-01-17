
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from linearize_handler import LinearizeHandler

import numpy as np
import math

class TestLinearizeHandler(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        self.bezier_curve = CubicBezierCurve()
        self.bezier_curve.append(bezier_ctrl_p)
        self.bezier_curve.append(bezier_ctrl_p)

    #end

    def test_linearize(self):

        # CubicBezierCurve of 90degree arc (radius=100)
        p0 = Point(100.0,                              0.0)
        p1 = Point(100.0,                              400.0*( math.sqrt(2.0) - 1.0 )/3.0)
        p2 = Point(400.0*( math.sqrt(2.0) - 1.0 )/3.0, 100.0)
        p3 = Point(0.0,                                100.0)
        ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        curve = CubicBezierCurve()
        curve.append(ctrl_p)

        linearize_handler = LinearizeHandler(options={"micro_segment_length":0.1})

        linear_approximate_curve = linearize_handler.process(curve.ctrl_p_set)

        origin = Point(0.0, 0.0)
        for ctrl_p in linear_approximate_curve:
            distance_from_origin = round( origin.distance(ctrl_p.s) )
            self.assertEqual(distance_from_origin, 100)
        #end

        # linearize_handler.__approximate_linear_curve(0, 0, 0) # <- cannot call private method
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

