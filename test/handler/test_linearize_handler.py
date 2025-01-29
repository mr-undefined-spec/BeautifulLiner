
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from linearize_handler import LinearizeHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import handler_mocks

import unittest

import numpy as np
import math

class TestLinearizeHandler(unittest.TestCase):
    def setUp(self):
        self.layer_set = handler_mocks.create_mock_layer_set_of_cubic_bezier_curve_arc()

    #end

    def test_linearize(self):
        linearize_handler = LinearizeHandler(options={"micro_segment_length":0.1})

        linearized_layer_set = linearize_handler.process(self.layer_set)

        for layer in linearized_layer_set:
            for curve_set in layer:
                for curve in curve_set:
                    for ctrl_p in curve:
                        delta_x = ctrl_p.start.x - 0.0
                        delta_y = ctrl_p.start.y - 0.0
                        distance_from_origin = round( math.sqrt(delta_x*delta_x + delta_y*delta_y) )
                        self.assertEqual(distance_from_origin, 100)
                    #end
                #end
            #end
        #end
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

