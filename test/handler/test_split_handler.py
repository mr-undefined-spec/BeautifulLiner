import unittest

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from point import Point

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from split_handler import SplitHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import model_mocks
import handler_mocks
from handler_mocks import ArcDirection


class TestSplitHandler(unittest.TestCase):
    def setUp(self):

        curve_1 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        curve_2 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0, 200.0, 180.0, 270.0, 100, ArcDirection.COUNTER_CLOCKWISE)
        curve_3 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0, -200.0, 200.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)

        the_curve = LinearApproximateCurve()
        for ctrl_p_1 in curve_1:
            the_curve.append(ctrl_p_1)
        #end
        for ctrl_p_2 in curve_2:
            the_curve.append(ctrl_p_2)
        #end
        for ctrl_p_3 in curve_3:
            the_curve.append(ctrl_p_3)
        #end

        self.curve = the_curve
    #end


    def test_split(self):
        #curve_orientations = [1, 1, 1, -1, -1, -1, 1, 1, 1]

        split_curve_ranges = SplitHandler.process(self.curve, 0)

        self.assertEqual(split_curve_ranges, [(0, 100), (100, 201), (201, 301)])
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end

