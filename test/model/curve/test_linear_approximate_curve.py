
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
from point import Point
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from linear_approximate_curve import LinearApproximateCurve
import unittest

import numpy as np
import math

class TestCurve(unittest.TestCase):
    def setUp(self):
        lin_p0 = Point(0.0, 0.0)
        lin_p1 = Point(1.0, 1.0)
        lin_p2 = Point(1.0, 0.0)
        lin_p3 = Point(0.0, 1.0)
        lin_p4 = Point(2.0, 1.0)

        linear_ctrl_p_0_1 = LinearApproximateCurveControlPoint(lin_p0, lin_p1)
        linear_ctrl_p_2_3 = LinearApproximateCurveControlPoint(lin_p2, lin_p3)
        linear_ctrl_p_2_4 = LinearApproximateCurveControlPoint(lin_p2, lin_p4)

        self.linear_curve = LinearApproximateCurve()
        self.linear_curve.append(linear_ctrl_p_0_1)
        self.linear_curve.append(linear_ctrl_p_2_3)
        self.linear_curve.append(linear_ctrl_p_2_4)

    #end
    def test_init_and_getitem(self):
        self.assertEqual(self.linear_curve[0].s.x, 0.0)
        self.assertEqual(self.linear_curve[0].s.y, 0.0)
        self.assertEqual(self.linear_curve[0].e.x, 1.0)
        self.assertEqual(self.linear_curve[0].e.y, 1.0)

        self.assertEqual(self.linear_curve[1].s.x, 1.0)
        self.assertEqual(self.linear_curve[1].s.y, 0.0)
        self.assertEqual(self.linear_curve[1].e.x, 0.0)
        self.assertEqual(self.linear_curve[1].e.y, 1.0)
    #end


    """

    def test_create_sequential_points(self):
        self.linear_curve.create_sequential_points()
        self.assertAlmostEqual(self.linear_curve.sequential_points[0].x, 0.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[0].y, 0.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[1].x, 1.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[1].y, 0.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[2].x, 1.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[2].y, 0.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[3].x, 2.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[3].y, 1.0)
    #end
    """

    def test_append(self):
        p5 = Point(11.0, 22.0)
        p6 = Point(111.0, 222.0)

        linear_ctrl_p_5_6 = LinearApproximateCurveControlPoint(p5, p6)
        
        self.linear_curve.append(linear_ctrl_p_5_6)
        self.assertEqual(self.linear_curve[3].s.x, 11.0)
        self.assertEqual(self.linear_curve[3].s.y, 22.0)
        self.assertEqual(self.linear_curve[3].e.x, 111.0)
        self.assertEqual(self.linear_curve[3].e.y, 222.0)
    #end

    def test_iter_and_next(self):
        s = ""
        for segment in self.linear_curve:
            s += str(segment)
        #end
        the_answer = "0.000 0.000\n1.000 1.000\n1.000 0.000\n0.000 1.000\n1.000 0.000\n2.000 1.000\n"
        self.assertEqual(s, the_answer)
    #end


    def test_create_intersect_judge_rectangle(self):
        # linear_curve
        self.linear_curve.create_intersect_judge_rectangle()
        self.assertEqual( self.linear_curve.rect.q.x, 0.0 )
        self.assertEqual( self.linear_curve.rect.q.y, 0.0 )
        self.assertEqual( self.linear_curve.rect.z.x, 0.0 )
        self.assertEqual( self.linear_curve.rect.z.y, 1.0 )
        self.assertEqual( self.linear_curve.rect.p.x, 2.0 )
        self.assertEqual( self.linear_curve.rect.p.y, 0.0 )
        self.assertEqual( self.linear_curve.rect.m.x, 2.0 )
        self.assertEqual( self.linear_curve.rect.m.y, 1.0 )
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

