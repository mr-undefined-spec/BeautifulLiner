
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
import mocks

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
from cubic_bezier_curve import CubicBezierCurve
import unittest

class TestCubicBezierCurve(unittest.TestCase):
    def setUp(self):
        p0 = mocks.create_mock_point(0.0, 0.0)
        p1 = mocks.create_mock_point(1.0, 2.0)
        p2 = mocks.create_mock_point(10.0, 20.0)
        p3 = mocks.create_mock_point(100.0, 200.0)
        bezier_ctrl_p = mocks.create_mock_cubic_bezier_control_point(p0, p1, p2, p3)
        #bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        self.bezier_curve = CubicBezierCurve()
        self.bezier_curve.append(bezier_ctrl_p)
        self.bezier_curve.append(bezier_ctrl_p)
    #end

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
        p0 = mocks.create_mock_point(0.0, 0.0)
        p1 = mocks.create_mock_point(1.0, 2.0)
        p4 = mocks.create_mock_point(11.0, 22.0)
        p5 = mocks.create_mock_point(111.0, 222.0)
        bezier_ctrl_p = mocks.create_mock_cubic_bezier_control_point(p0, p1, p4, p5)
        
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

if __name__ == '__main__':
    unittest.main()
#end

