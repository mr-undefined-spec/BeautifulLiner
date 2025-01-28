import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../helper'))
import model_mocks

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
from single_curve_set import SingleCurveSet
from curve import Curve

import unittest

import numpy as np
import math

class TestSingleCurveSet(unittest.TestCase):
    def setUp(self):
        p0 = model_mocks.create_mock_point(0.0, 0.0)
        p1 = model_mocks.create_mock_point(1.0, 1.0)
        p2 = model_mocks.create_mock_point(1.0, 0.0)
        p3 = model_mocks.create_mock_point(0.0, 1.0)
        p4 = model_mocks.create_mock_point(2.0, 1.0)

        linear_ctrl_p_0_1 = model_mocks.create_mock_linear_approximate_curve_control_point(p0, p1)
        linear_ctrl_p_2_3 = model_mocks.create_mock_linear_approximate_curve_control_point(p2, p3)
        linear_ctrl_p_2_4 = model_mocks.create_mock_linear_approximate_curve_control_point(p2, p4)
        linear_ctrl_p_set = []
        linear_ctrl_p_set.append(linear_ctrl_p_0_1)
        linear_ctrl_p_set.append(linear_ctrl_p_2_3)
        linear_ctrl_p_set.append(linear_ctrl_p_2_4)

        linear_approximate_curve = model_mocks.create_mock_linear_approximate_curve(linear_ctrl_p_set)

        self.single_curve_set = SingleCurveSet(linear_approximate_curve)
    #end

    def test_init_and_getitem(self):
        self.assertEqual(isinstance(self.single_curve_set[0], Curve), True)
    #end

    def test_len(self):
        self.assertEqual(len(self.single_curve_set), 1)
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

