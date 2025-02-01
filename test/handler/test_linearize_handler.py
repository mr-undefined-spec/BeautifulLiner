
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from linearize_handler import LinearizeHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import handler_mocks
import model_mocks

import unittest

import numpy as np
import math

class TestLinearizeHandler(unittest.TestCase):
    def setUp(self):
        self.layer_set = handler_mocks.create_mock_layer_set_of_cubic_bezier_curve_arc()

    #end

    def test_linearize(self):
        # CubicBezierCurve of 90degree arc (radius=100)
        p0 = model_mocks.create_mock_point(100.0,                              0.0)
        p1 = model_mocks.create_mock_point(100.0,                              400.0*( math.sqrt(2.0) - 1.0 )/3.0)
        p2 = model_mocks.create_mock_point(400.0*( math.sqrt(2.0) - 1.0 )/3.0, 100.0)
        p3 = model_mocks.create_mock_point(0.0,                                100.0)
        ctrl_p = model_mocks.create_mock_cubic_bezier_control_point(p0, p1, p2, p3)

        linearize_handler = LinearizeHandler(options={"micro_segment_length":0.1})
        linearized_points = linearize_handler.get_points_of_approximate_linear_curve(ctrl_p, True, 0.1)

        for p in linearized_points:
            delta_x = p.x - 0.0
            delta_y = p.y - 0.0
            distance_from_origin = round( math.sqrt(delta_x*delta_x + delta_y*delta_y) )
            self.assertEqual(distance_from_origin, 100)
        #end
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

