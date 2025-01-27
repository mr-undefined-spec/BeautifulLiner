
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
import mocks

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
from linear_approximate_curve import LinearApproximateCurve
import unittest

class TestCurve(unittest.TestCase):
    def setUp(self):
        p0 = mocks.create_mock_point(0.0, 0.0)
        p1 = mocks.create_mock_point(1.0, 1.0)
        p2 = mocks.create_mock_point(1.0, 0.0)
        p3 = mocks.create_mock_point(0.0, 1.0)
        p4 = mocks.create_mock_point(2.0, 1.0)

        linear_ctrl_p_0_1 = mocks.create_mock_linear_approximate_curve_control_point(p0, p1)
        linear_ctrl_p_2_3 = mocks.create_mock_linear_approximate_curve_control_point(p2, p3)
        linear_ctrl_p_2_4 = mocks.create_mock_linear_approximate_curve_control_point(p2, p4)
        linear_ctrl_p_set = []
        linear_ctrl_p_set.append(linear_ctrl_p_0_1)
        linear_ctrl_p_set.append(linear_ctrl_p_2_3)
        linear_ctrl_p_set.append(linear_ctrl_p_2_4)

        aaa = mocks.create_mock_linear_approximate_curve(linear_ctrl_p_set)
        print(aaa[0])

        self.linear_approximate_curve = LinearApproximateCurve()
        self.linear_approximate_curve.append(linear_ctrl_p_0_1)
        self.linear_approximate_curve.append(linear_ctrl_p_2_3)
        self.linear_approximate_curve.append(linear_ctrl_p_2_4)

    #end
    def test_init_and_getitem(self):
        self.assertEqual(self.linear_approximate_curve[0].start.x, 0.0)
        self.assertEqual(self.linear_approximate_curve[0].start.y, 0.0)
        self.assertEqual(self.linear_approximate_curve[0].end.x, 1.0)
        self.assertEqual(self.linear_approximate_curve[0].end.y, 1.0)

        self.assertEqual(self.linear_approximate_curve[1].start.x, 1.0)
        self.assertEqual(self.linear_approximate_curve[1].start.y, 0.0)
        self.assertEqual(self.linear_approximate_curve[1].end.x, 0.0)
        self.assertEqual(self.linear_approximate_curve[1].end.y, 1.0)
    #end


    """

    def test_create_sequential_points(self):
        self.linear_approximate_curve.create_sequential_points()
        self.assertAlmostEqual(self.linear_approximate_curve.sequential_points[0].x, 0.0)
        self.assertAlmostEqual(self.linear_approximate_curve.sequential_points[0].y, 0.0)
        self.assertAlmostEqual(self.linear_approximate_curve.sequential_points[1].x, 1.0)
        self.assertAlmostEqual(self.linear_approximate_curve.sequential_points[1].y, 0.0)
        self.assertAlmostEqual(self.linear_approximate_curve.sequential_points[2].x, 1.0)
        self.assertAlmostEqual(self.linear_approximate_curve.sequential_points[2].y, 0.0)
        self.assertAlmostEqual(self.linear_approximate_curve.sequential_points[3].x, 2.0)
        self.assertAlmostEqual(self.linear_approximate_curve.sequential_points[3].y, 1.0)
    #end
    """

    def test_append(self):
        p5 = mocks.create_mock_point(11.0, 22.0)
        p6 = mocks.create_mock_point(111.0, 222.0)

        #linear_ctrl_p_5_6 = LinearApproximateCurveControlPoint(p5, p6)
        linear_ctrl_p_5_6 = mocks.create_mock_linear_approximate_curve_control_point(mocks.create_mock_point(11.0, 22.0), mocks.create_mock_point(111.0, 222.0))
        
        self.linear_approximate_curve.append(linear_ctrl_p_5_6)
        self.assertEqual(self.linear_approximate_curve[3].start.x, 11.0)
        self.assertEqual(self.linear_approximate_curve[3].start.y, 22.0)
        self.assertEqual(self.linear_approximate_curve[3].end.x, 111.0)
        self.assertEqual(self.linear_approximate_curve[3].end.y, 222.0)
    #end

    def test_iter_and_next(self):
        s = ""
        for segment in self.linear_approximate_curve:
            s += str(segment)
        #end
        the_answer = "0.000 0.000\n1.000 1.000\n1.000 0.000\n0.000 1.000\n1.000 0.000\n2.000 1.000\n"
        self.assertEqual(s, the_answer)
    #end


    def test_create_intersect_judge_rectangle(self):
        # linear_approximate_curve
        self.linear_approximate_curve.create_intersect_judge_rectangle()
        self.assertEqual( self.linear_approximate_curve.rect.q.x, 0.0 )
        self.assertEqual( self.linear_approximate_curve.rect.q.y, 0.0 )
        self.assertEqual( self.linear_approximate_curve.rect.z.x, 0.0 )
        self.assertEqual( self.linear_approximate_curve.rect.z.y, 1.0 )
        self.assertEqual( self.linear_approximate_curve.rect.p.x, 2.0 )
        self.assertEqual( self.linear_approximate_curve.rect.p.y, 0.0 )
        self.assertEqual( self.linear_approximate_curve.rect.m.x, 2.0 )
        self.assertEqual( self.linear_approximate_curve.rect.m.y, 1.0 )
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

