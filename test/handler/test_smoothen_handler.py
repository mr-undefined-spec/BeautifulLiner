
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from linear_approximate_curve import LinearApproximateCurve
from curve_set import CurveSet

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

class TestSplitHandler(unittest.TestCase):
    def setUp(self):

        curve_1 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        curve_2 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0, 200.0, 180.0, 270.0, 100, ArcDirection.COUNTER_CLOCKWISE)
        curve_3 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0, -200.0, 200.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)

        curve_set = model_mocks.create_mock_curve_set([curve_1, curve_2, curve_3])
        layer = model_mocks.create_mock_layer([curve_set])
        self.layer_set = [layer]
        
        #handler_mocks.create_mock_layer_set_of_arc_as_linear_approximate_curve(100.0, 0.0, 0.0, 0.0, 90.0, 100)

    #end

    def test_split(self):

        the_answer = ["100.000 0.000\n101.572 53.551\n53.551 101.572\n0.000 100.000\n",
                        "-0.000 100.000\n-53.551 98.428\n-101.572 146.449\n-100.000 200.000\n",
                        "-100.000 200.000\n-98.428 253.551\n-146.449 301.572\n-200.000 300.000\n"]

        the_answer_index = 0

        smoothen_handler = SmoothenHandler()

        smoothen_layer_set = smoothen_handler.process(self.layer_set)
        for layer in smoothen_layer_set:
            for curve_set in layer:
                #print("[")
                for curve in curve_set:
                    #print(curve)
                    #print("[")
                    for ctrl_p in curve:
                        #print('"' + str(ctrl_p) + '",')
                        self.assertEqual(str(ctrl_p), the_answer[the_answer_index])
                        the_answer_index += 1
                    #end
                    #print("],")
                #end
                #print("]")
            #end
        #end
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

