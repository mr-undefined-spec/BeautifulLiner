
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../helper'))
import model_mocks

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint

import unittest

class TestCubicBezierCurveControlPoint(unittest.TestCase):
    def setUp(self):
        p0 = model_mocks.create_mock_point(0.0, 0.0)
        p1 = model_mocks.create_mock_point(1.0, 2.0)
        p2 = model_mocks.create_mock_point(10.0, 20.0)
        p3 = model_mocks.create_mock_point(100.0, 200.0)

        self.bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)
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
    #end

    def test_max_min_in_cubic_bezier(self):
        self.assertEqual(self.bezier_ctrl_p.get_max_x(), 100.0)
        self.assertEqual(self.bezier_ctrl_p.get_max_y(), 200.0)
        self.assertEqual(self.bezier_ctrl_p.get_min_x(), 0.0)
        self.assertEqual(self.bezier_ctrl_p.get_min_y(), 0.0)
    #end

    def test_str(self):
        the_answer = "0.000 0.000\n1.000 2.000\n10.000 20.000\n100.000 200.000\n"
        self.assertEqual( str(self.bezier_ctrl_p), the_answer )
    #end

    def test_to_str(self):
        is_going_first_true      = True
        is_going_first_false     = False
        is_returning_first_true  = True
        is_returning_first_false = False

        self.assertEqual( self.bezier_ctrl_p.to_str(is_going_first_true, is_returning_first_true), "M 0.000 0.000 L 0.000 0.000 C 1.000 2.000 10.000 20.000 100.000 200.000 " )
        self.assertEqual( self.bezier_ctrl_p.to_str(is_going_first_true, is_returning_first_false), "M 0.000 0.000 C 1.000 2.000 10.000 20.000 100.000 200.000 " )
        self.assertEqual( self.bezier_ctrl_p.to_str(is_going_first_false, is_returning_first_true), "L 0.000 0.000 C 1.000 2.000 10.000 20.000 100.000 200.000 " )
        self.assertEqual( self.bezier_ctrl_p.to_str(is_going_first_false, is_returning_first_false), "C 1.000 2.000 10.000 20.000 100.000 200.000 " )
    #end

    def test_raise_error_with_set_p0_to_p3_as_int(self):
        p = model_mocks.create_mock_point(100.0, 200.0)

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

