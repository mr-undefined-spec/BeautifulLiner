
import os
import sys

import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
from point import Point
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

import unittest
from unittest.mock import MagicMock

class TestLinearApproximateCurveControlPoint(unittest.TestCase):
    def setUp(self):
        lin_p0 = MagicMock(spec=Point, x=0.0, y=0.0)
        lin_p0.__str__.return_value = "0.000 0.000"
        lin_p1 = MagicMock(spec=Point, x=1.0, y=1.0)
        lin_p1.__str__.return_value = "1.000 1.000"
        lin_p2 = MagicMock(spec=Point, x=1.0, y=0.0)
        lin_p2.__str__.return_value = "1.000 0.000"
        lin_p3 = MagicMock(spec=Point, x=0.0, y=1.0)
        lin_p3.__str__.return_value = "0.000 1.000"
        lin_p4 = MagicMock(spec=Point, x=2.0, y=1.0)
        lin_p4.__str__.return_value = "2.000 1.000"
        #lin_p0 = Point(0.0, 0.0)
        #lin_p1 = Point(1.0, 1.0)
        #lin_p2 = Point(1.0, 0.0)
        #lin_p3 = Point(0.0, 1.0)
        #lin_p4 = Point(2.0, 1.0)

        self.linear_ctrl_p_0_1 = LinearApproximateCurveControlPoint(lin_p0, lin_p1)
        self.linear_ctrl_p_2_3 = LinearApproximateCurveControlPoint(lin_p2, lin_p3)
        self.linear_ctrl_p_2_4 = LinearApproximateCurveControlPoint(lin_p2, lin_p4)
        self.linear_ctrl_p_2_1 = LinearApproximateCurveControlPoint(lin_p2, lin_p1)
    #end

    def test_init(self):
        self.assertEqual(self.linear_ctrl_p_0_1.s.x, 0.0)
        self.assertEqual(self.linear_ctrl_p_0_1.s.y, 0.0)
        self.assertEqual(self.linear_ctrl_p_0_1.e.x, 1.0)
        self.assertEqual(self.linear_ctrl_p_0_1.e.y, 1.0)
    #end

    def test_max_min_in_cubic_bezier(self):
        self.assertEqual(self.linear_ctrl_p_0_1.get_max_x(), 1.0)
        self.assertEqual(self.linear_ctrl_p_0_1.get_max_y(), 1.0)
        self.assertEqual(self.linear_ctrl_p_0_1.get_min_x(), 0.0)
        self.assertEqual(self.linear_ctrl_p_0_1.get_min_y(), 0.0)
    #end

    def test_str(self):
        the_answer_2 = "0.000 0.000\n1.000 1.000\n"
        self.assertEqual( str(self.linear_ctrl_p_0_1), the_answer_2 )
    #end

    def test_to_str(self):
        is_first_ctrl_p_true  = True
        is_first_ctrl_p_false = False

        self.assertEqual( self.linear_ctrl_p_0_1.to_str(is_first_ctrl_p_true), "M 0.000 0.000 L 1.000 1.000 " )
        self.assertEqual( self.linear_ctrl_p_0_1.to_str(is_first_ctrl_p_false), "L 1.000 1.000 " )
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

    def test_get_distance_to_point(self):
        target_point = MagicMock(spec=Point, x=1.0, y=0.0)
        the_distance = self.linear_ctrl_p_0_1.get_distance_to_point(target_point)
        self.assertAlmostEqual(the_distance, math.sqrt(2.0)/2.0)
    #end

    def test_get_min_distance_to_segment(self):
        the_distance = self.linear_ctrl_p_0_1.get_min_distance_to_segment(self.linear_ctrl_p_2_4)
        self.assertAlmostEqual(the_distance, math.sqrt(2.0)/2.0)
    #end

    def test_get_average_distance_to_segment(self):
        the_distance = self.linear_ctrl_p_0_1.get_average_distance_to_segment(self.linear_ctrl_p_2_1)
        self.assertAlmostEqual(the_distance, (math.sqrt(2.0)+2.0)/8.0)
        # 
        #       p1
        #       *
        #      /|
        #     / |
        #    /  |
        #   /   |
        #  *    *
        # p0    p2
        #
        # the distance between p0 and segment_p2_p1 is 1.0
        # the distance between p1 and segment_p2_p1 is 0.0
        # the distance between p2 and segment_p0_p1 is sqrt(2)/2.0
        # the distance between p1 and segment_p0_p1 is 0.0
        # the average distance is (sqrt(2)+2.0)/8.0
        # 
    #end

    def test_get_perpendicular_intersection_point_from_point(self):
        #        (1, 1)
        #       p1
        #       *
        #      /
        #     +  <-- perpendicular intersection point
        #    / \  (0.5, 0.5)
        #   /   \ 
        #  *     *
        # p0     p2
        # (0, 0) (1, 0)
        # 
        #
        target_point = MagicMock(spec=Point, x=1.0, y=0.0)
        the_point = self.linear_ctrl_p_0_1.get_perpendicular_intersection_point_from_point(target_point)
        self.assertAlmostEqual(the_point.x, 0.5)
        self.assertAlmostEqual(the_point.y, 0.5)
    #end



#end


if __name__ == '__main__':
    unittest.main()
#end

