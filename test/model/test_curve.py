
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from point import Point
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint
from curve import CubicBezierCurve
from curve import LinearApproximateCurve
import unittest

class TestCurve(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        self.bezier_curve = CubicBezierCurve()
        self.bezier_curve.append(bezier_ctrl_p)
        self.bezier_curve.append(bezier_ctrl_p)

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

    def test_init_segment_set(self):
        self.assertEqual(self.linear_curve[0].s.x, 0.0)
        self.assertEqual(self.linear_curve[0].s.y, 0.0)
        self.assertEqual(self.linear_curve[0].e.x, 1.0)
        self.assertEqual(self.linear_curve[0].e.y, 1.0)

        self.assertEqual(self.linear_curve[1].s.x, 1.0)
        self.assertEqual(self.linear_curve[1].s.y, 0.0)
        self.assertEqual(self.linear_curve[1].e.x, 0.0)
        self.assertEqual(self.linear_curve[1].e.y, 1.0)
    #end

    def test_init_cubic_bezier_curve_set(self):
        self.assertEqual(self.bezier_curve[0].p0.x, 0.0)
        self.assertEqual(self.bezier_curve[0].p0.y, 0.0)
        self.assertEqual(self.bezier_curve[0].p1.x, 1.0)
        self.assertEqual(self.bezier_curve[0].p1.y, 2.0)
        self.assertEqual(self.bezier_curve[0].p2.x, 10.0)
        self.assertEqual(self.bezier_curve[0].p2.y, 20.0)
        self.assertEqual(self.bezier_curve[0].p3.x, 100.0)
        self.assertEqual(self.bezier_curve[0].p3.y, 200.0)
    #end

    def test_append_segment_set(self):
        p5 = Point(11.0, 22.0)
        p6 = Point(111.0, 222.0)

        linear_ctrl_p_5_6 = LinearApproximateCurveControlPoint(p5, p6)
        
        self.linear_curve.append(linear_ctrl_p_5_6)
        self.assertEqual(self.linear_curve[3].s.x, 11.0)
        self.assertEqual(self.linear_curve[3].s.y, 22.0)
        self.assertEqual(self.linear_curve[3].e.x, 111.0)
        self.assertEqual(self.linear_curve[3].e.y, 222.0)
    #end

    def test_append_cubic_bezier_curve(self):
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

    def test_iter_linear(self):
        s = ""
        for segment in self.linear_curve:
            s += str(segment)
        #end
        the_answer = "0.000 0.000\n1.000 1.000\n1.000 0.000\n0.000 1.000\n1.000 0.000\n2.000 1.000\n"
        self.assertEqual(s, the_answer)
    #end

    def test_iter_bezier(self):
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

