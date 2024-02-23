
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from point import Point
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint
import unittest

class TestControlPoint(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        self.bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        lin_p0 = Point(0.0, 0.0)
        lin_p1 = Point(1.0, 1.0)
        lin_p2 = Point(1.0, 0.0)
        lin_p3 = Point(0.0, 1.0)
        lin_p4 = Point(2.0, 1.0)

        self.linear_ctrl_p_0_1 = LinearApproximateCurveControlPoint(lin_p0, lin_p1)
        self.linear_ctrl_p_2_3 = LinearApproximateCurveControlPoint(lin_p2, lin_p3)
        self.linear_ctrl_p_2_4 = LinearApproximateCurveControlPoint(lin_p2, lin_p4)
    #end

    def test_init(self):
        self.assertEqual(self.bezier_ctrl_p.p0.x, 0.0)
        self.assertEqual(self.bezier_ctrl_p.p0.y, 0.0)
        self.assertEqual(self.bezier_ctrl_p.p1.x, 1.0)
        self.assertEqual(self.bezier_ctrl_p.p1.y, 2.0)
        self.assertEqual(self.bezier_ctrl_p.p2.x, 10.0)
        self.assertEqual(self.bezier_ctrl_p.p2.y, 20.0)
        self.assertEqual(self.bezier_ctrl_p.p3.x, 100.0)
        self.assertEqual(self.bezier_ctrl_p.p3.y, 200.0)

        self.assertEqual(self.linear_ctrl_p_0_1.s.x, 0.0)
        self.assertEqual(self.linear_ctrl_p_0_1.s.y, 0.0)
        self.assertEqual(self.linear_ctrl_p_0_1.e.x, 1.0)
        self.assertEqual(self.linear_ctrl_p_0_1.e.y, 1.0)
    #end

    def test_max_min_in_cubic_bezier(self):
        self.assertEqual(self.bezier_ctrl_p.get_max_x(), 100.0)
        self.assertEqual(self.bezier_ctrl_p.get_max_y(), 200.0)
        self.assertEqual(self.bezier_ctrl_p.get_min_x(), 0.0)
        self.assertEqual(self.bezier_ctrl_p.get_min_y(), 0.0)
        
        self.assertEqual(self.linear_ctrl_p_0_1.get_max_x(), 1.0)
        self.assertEqual(self.linear_ctrl_p_0_1.get_max_y(), 1.0)
        self.assertEqual(self.linear_ctrl_p_0_1.get_min_x(), 0.0)
        self.assertEqual(self.linear_ctrl_p_0_1.get_min_y(), 0.0)
    #end

    def test_str(self):
        the_answer = "0.000 0.000\n1.000 2.000\n10.000 20.000\n100.000 200.000\n"
        self.assertEqual( str(self.bezier_ctrl_p), the_answer )

        the_answer_2 = "0.000 0.000\n1.000 1.000\n"
        self.assertEqual( str(self.linear_ctrl_p_0_1), the_answer_2 )
    #end

    def test_to_svg(self):
        is_going_first_true      = True
        is_going_first_false     = False
        is_returning_first_true  = True
        is_returning_first_false = False

        self.assertEqual( self.bezier_ctrl_p.to_svg(is_going_first_true, is_returning_first_true), "M 0.000 0.000 L 0.000 0.000 C 1.000 2.000 10.000 20.000 100.000 200.000 " )
        self.assertEqual( self.bezier_ctrl_p.to_svg(is_going_first_true, is_returning_first_false), "M 0.000 0.000 C 1.000 2.000 10.000 20.000 100.000 200.000 " )
        self.assertEqual( self.bezier_ctrl_p.to_svg(is_going_first_false, is_returning_first_true), "L 0.000 0.000 C 1.000 2.000 10.000 20.000 100.000 200.000 " )
        self.assertEqual( self.bezier_ctrl_p.to_svg(is_going_first_false, is_returning_first_false), "C 1.000 2.000 10.000 20.000 100.000 200.000 " )

        is_first_ctrl_p_true  = True
        is_first_ctrl_p_false = False

        self.assertEqual( self.linear_ctrl_p_0_1.to_svg(is_first_ctrl_p_true), "M 0.000 0.000 L 1.000 1.000 " )
        self.assertEqual( self.linear_ctrl_p_0_1.to_svg(is_first_ctrl_p_false), "L 1.000 1.000 " )
    #end

    def test_intersection(self):
        inter_p_01_23 = self.linear_ctrl_p_0_1.intersection(self.linear_ctrl_p_2_3)
        self.assertAlmostEqual(inter_p_01_23.x, 0.5)
        self.assertAlmostEqual(inter_p_01_23.y, 0.5)

        self.assertEqual(self.linear_ctrl_p_0_1.is_intersection(self.linear_ctrl_p_2_4), False)
    #end

    def test_get_rect_tuple(self):
        the_tuple = self.linear_ctrl_p_0_1.get_rect_tuple()

        self.assertEqual( the_tuple[0], 0.0 )
        self.assertEqual( the_tuple[1], 0.0 )
        self.assertEqual( the_tuple[2], 1.0 )
        self.assertEqual( the_tuple[3], 1.0 )
    #end

    def test_raise_error_with_set_p0_to_p3_as_int(self):
        p = Point(1.0, 2.1)

        with self.assertRaises(TypeError) as e:
            bezier_ctrl_p = CubicBezierCurveControlPoint(0, p, p, p)
        #end with
        self.assertEqual(e.exception.args[0], 'p0 must be Point')

        with self.assertRaises(TypeError) as e:
            bezier_ctrl_p = CubicBezierCurveControlPoint(p, 0, p, p)
        #end with
        self.assertEqual(e.exception.args[0], 'p1 must be Point')

        with self.assertRaises(TypeError) as e:
            bezier_ctrl_p = CubicBezierCurveControlPoint(p, p, 0, p)
        #end with
        self.assertEqual(e.exception.args[0], 'p2 must be Point')

        with self.assertRaises(TypeError) as e:
            bezier_ctrl_p = CubicBezierCurveControlPoint(p, p, p, 0)
        #end with
        self.assertEqual(e.exception.args[0], 'p3 must be Point')
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

