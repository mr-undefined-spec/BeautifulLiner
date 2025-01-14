
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
import unittest

import numpy as np
import math

class TestCubicBezierCurve(unittest.TestCase):
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

    """

    def test_create_intersect_judge_rectangle(self):
        #bezier_curve
        self.bezier_curve.create_intersect_judge_rectangle()
        self.assertEqual( self.bezier_curve.rect.q.x, 0.0 )
        self.assertEqual( self.bezier_curve.rect.q.y, 0.0 )
        self.assertEqual( self.bezier_curve.rect.z.x, 0.0 )
        self.assertEqual( self.bezier_curve.rect.z.y, 200.0 )
        self.assertEqual( self.bezier_curve.rect.p.x, 100.0 )
        self.assertEqual( self.bezier_curve.rect.p.y, 0.0 )
        self.assertEqual( self.bezier_curve.rect.m.x, 100.0 )
        self.assertEqual( self.bezier_curve.rect.m.y, 200.0 )
    #end
    """

    def test_init_and_getitem(self):
        self.assertEqual(self.bezier_curve[0].p0.x, 0.0)
        self.assertEqual(self.bezier_curve[0].p0.y, 0.0)
        self.assertEqual(self.bezier_curve[0].p1.x, 1.0)
        self.assertEqual(self.bezier_curve[0].p1.y, 2.0)
        self.assertEqual(self.bezier_curve[0].p2.x, 10.0)
        self.assertEqual(self.bezier_curve[0].p2.y, 20.0)
        self.assertEqual(self.bezier_curve[0].p3.x, 100.0)
        self.assertEqual(self.bezier_curve[0].p3.y, 200.0)
    #end

    def test_append(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p4 = Point(11.0, 22.0)
        p5 = Point(111.0, 222.0)

        bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p4, p5)
        
        self.bezier_curve.append(bezier_ctrl_p)
        self.assertEqual(self.bezier_curve[2].p2.x, 11.0)
        self.assertEqual(self.bezier_curve[2].p2.y, 22.0)
        self.assertEqual(self.bezier_curve[2].p3.x, 111.0)
        self.assertEqual(self.bezier_curve[2].p3.y, 222.0)
    #end

    def test_len(self):
        self.assertEqual(len(self.bezier_curve), 2)
    #end

    def test_iter_and_next(self):
        s = ""
        for curve in self.bezier_curve:
            s += str(curve)
        #end
        the_answer = "0.000 0.000\n1.000 2.000\n10.000 20.000\n100.000 200.000\n0.000 0.000\n1.000 2.000\n10.000 20.000\n100.000 200.000\n"
        self.assertEqual(s, the_answer)
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

