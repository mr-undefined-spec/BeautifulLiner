
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from linearize_handler import LinearizeHandler
from smoothen_handler import SmoothenHandler
from residual_calculate_handler import ResidualCalculateHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import handler_mocks
import model_mocks

import unittest

import numpy as np
import math

class TestResidualCalculateHandler(unittest.TestCase):
    def setUp(self):
        self.layer_set = handler_mocks.create_mock_layer_set_of_cubic_bezier_curve_arc()

    #end

    def test_residual_calculate(self):
        ctrl_p_set_1 = []
        linear_approximate_curve_1 = LinearApproximateCurve()
        for i in range(100):
            mock_start_p = model_mocks.create_mock_point(float(i), 0.0)
            mock_end_p = model_mocks.create_mock_point(float(i+1), 0.0)
            linear_approximate_curve_control_point = model_mocks.create_mock_linear_approximate_curve_control_point(mock_start_p, mock_end_p)
            linear_approximate_curve_1.append(linear_approximate_curve_control_point)
        #end
        #linear_approximate_curve_1 = model_mocks.create_mock_linear_approximate_curve(ctrl_p_set_1)

        ctrl_p_set_2 = []
        linear_approximate_curve_2 = LinearApproximateCurve()
        for i in range(100):
            mock_start_p = model_mocks.create_mock_point(float(i), 1.0)
            mock_end_p = model_mocks.create_mock_point(float(i+1), 1.0)
            linear_approximate_curve_control_point = model_mocks.create_mock_linear_approximate_curve_control_point(mock_start_p, mock_end_p)
            linear_approximate_curve_2.append(linear_approximate_curve_control_point)
        #end
        #linear_approximate_curve_2 = model_mocks.create_mock_linear_approximate_curve(ctrl_p_set_2)

        residual_calculate_handler = ResidualCalculateHandler()
        residual = residual_calculate_handler.calculate_residual(linear_approximate_curve_1, linear_approximate_curve_2)
        #print(residual)

        self.assertEqual(residual, 100.0)

    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

