import unittest
import math

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from linearize_handler import LinearizeHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import handler_mocks
import model_mocks

class TestLinearizeHandler(unittest.TestCase):
    def setUp(self):
        self.layer_set = handler_mocks.create_mock_layer_set_of_cubic_bezier_curve_arc()

    #end

    def test_linearize(self):
        linear_approximate_curve = LinearizeHandler.process(self.layer_set[0][0], 0.1)


        for ctrl_p in linear_approximate_curve:
            delta_x = ctrl_p.start.x - 0.0
            delta_y = ctrl_p.start.y - 0.0
            distance_from_origin = round( math.sqrt(delta_x*delta_x + delta_y*delta_y) )
            self.assertEqual(distance_from_origin, 100)
        #end
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

