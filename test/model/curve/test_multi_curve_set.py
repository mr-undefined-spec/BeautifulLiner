import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
import mocks

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
from multi_curve_set import MultiCurveSet
from curve import Curve

import unittest

import numpy as np
import math

class TestSingleCurveSet(unittest.TestCase):
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

        linear_approximate_curve = mocks.create_mock_linear_approximate_curve(linear_ctrl_p_set)

        self.multi_curve_set = MultiCurveSet()
        self.multi_curve_set.append(linear_approximate_curve)
        self.multi_curve_set.append(linear_approximate_curve)
        self.multi_curve_set.append(linear_approximate_curve)
    #end

    def test_init_and_getitem(self):
        self.assertEqual(isinstance(self.multi_curve_set[0], Curve), True)
    #end

    def test_len(self):
        self.assertEqual(len(self.multi_curve_set), 3)
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end