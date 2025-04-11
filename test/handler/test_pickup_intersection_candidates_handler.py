import unittest

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from pickup_intersection_candidates_handler import PickupIntersectionCandidatesHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import model_mocks
import handler_mocks
from handler_mocks import ArcDirection

from unittest.mock import MagicMock

import numpy as np
import math

class TestPickupIntersectionCandidatesHandler(unittest.TestCase):
    def test_delete_edge(self):
        curve_1 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        curve_2 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,  100.0,   0.0,  90.0, 180.0, 100, ArcDirection.CLOCKWISE)
        curve_3 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0, 200.0, 180.0, 270.0, 100, ArcDirection.COUNTER_CLOCKWISE)
        curve_4 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0, -200.0, 200.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)

        candidates = PickupIntersectionCandidatesHandler.process(curve_1, [curve_1, curve_2, curve_3, curve_4])

        self.assertEqual(candidates[0], curve_2)

    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

