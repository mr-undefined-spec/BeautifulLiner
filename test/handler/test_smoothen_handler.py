
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/layer'))
from layer import Layer
from layer_set import LayerSet

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from smoothen_handler import SmoothenHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import model_mocks
import handler_mocks
from handler_mocks import ArcDirection

import unittest

import numpy as np
import math

class TestSmoothenHandler(unittest.TestCase):
    def setUp(self):

        self.curve_1 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        self.curve_2 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0, 200.0, 180.0, 270.0, 100, ArcDirection.COUNTER_CLOCKWISE)
        self.curve_3 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0, -200.0, 200.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)

    #end

    def test_smoothen(self):

        the_answer_1 = "100.000 0.000\n101.572 53.551\n53.551 101.572\n0.000 100.000\n"
        the_answer_2 = "-0.000 100.000\n-53.551 98.428\n-101.572 146.449\n-100.000 200.000\n"
        the_answer_3 = "-100.000 200.000\n-98.428 253.551\n-146.449 301.572\n-200.000 300.000\n"

        smoothened_curve_1 = SmoothenHandler.process(self.curve_1)
        smoothened_curve_2 = SmoothenHandler.process(self.curve_2)
        smoothened_curve_3 = SmoothenHandler.process(self.curve_3)

        self.assertEqual(str(smoothened_curve_1[0]), the_answer_1)
        self.assertEqual(str(smoothened_curve_2[0]), the_answer_2)
        self.assertEqual(str(smoothened_curve_3[0]), the_answer_3)

    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

